# orchestrator.py
from __future__ import annotations
from typing import List, Dict
import json
from crewai import Task, Crew, Process
from agents import analyst_news, analyst_tech, analyst_fund, portfolio_mgr

ORCH_PROMPT = """RUOLO: Orchestrator per analisi finanziarie multi‑agente.
AGENT DISPONIBILI:
- analyst_news: notizie & sentiment con fonti.
- analyst_tech: analisi tecnica (RSI, MA, volumi, supporti/resistenze, breakout) multi‑timeframe.
- analyst_fund: fondamentali (ultimi 4 trimestri, guidance, multipli, comparables, rischi).
- portfolio_mgr: impatto su portafoglio, rischio, ribilanciamenti e limiti di esposizione.

ISTRUZIONI:
1) Leggi la richiesta: \"\"\"{QUERY}\"\"\".
2) Determina l’intento tra: news | tech | fund | portfolio | misto.
3) Scegli il minor numero di agent necessari (1..4) e definisci una sequenza (plan).
4) Per ciascun step prepara un brief operativo molto specifico (ticker, timeframe, indicatori/KPI).
5) OUTPUT: JSON valido con le chiavi:
   {{
     "plan":[{{"agent":"<nome_agent>","brief":"<brief>"}}, ...],
     "tone":"prudente|neutro|didattico",
     "final_goal":"<obiettivo finale conciso>"
   }}
NON produrre testo discorsivo, solo JSON.
"""

def _fallback_plan(query: str) -> Dict:
    """Router molto semplice se il modello fallisce."""
    q = (query or "").lower()
    plan = []
    if any(k in q for k in ["news", "rumor", "notiz"]):
        plan.append({"agent": "analyst_news", "brief": f"Raccogli news rilevanti e sentiment su: '{query}'. Cita 3 fonti."})
    if any(k in q for k in ["tecnico", "rsi", "support", "resist", "grafico", "livelli"]):
        plan.append({"agent": "analyst_tech", "brief": f"Analizza tecnicamente '{query}' su 1D e 4H: RSI, MA50/200, supporti/resistenze, volumi."})
    if any(k in q for k in ["fondament", "utili", "eps", "pe ", "pe/", "p/e", "guidance", "multipli"]):
        plan.append({"agent": "analyst_fund", "brief": f"Riepiloga ultimi 4 trimestri e multipli per '{query}': EPS sorpresa, revenue YoY, P/E vs peer, rischi."})
    if any(k in q for k in ["portafoglio", "ribilanci", "rischio", "allocazione"]):
        plan.append({"agent": "portfolio_mgr", "brief": f"Valuta impatto su portafoglio e possibili ribilanci per richiesta: '{query}'."})

    if not plan:
        # default: tecnica + news
        plan = [
            {"agent": "analyst_tech", "brief": f"Analizza tecnicamente '{query}' su 1D e 4H: RSI, MA50/200, supporti/resistenze, volumi."},
            {"agent": "analyst_news", "brief": f"Raccogli news recenti e sentiment su: '{query}'. Cita 2-3 fonti."},
        ]
    return {"plan": plan, "tone": "prudente", "final_goal": "Sintesi per decisione operativa informata"}

def plan_from_llm(query: str, client) -> Dict:
    """Chiede al modello un piano JSON; se non è JSON valido, usa fallback."""
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},  # forza JSON
            messages=[
                {"role": "system", "content": "Sei un router di orchestrazione: restituisci SOLO JSON valido."},
                {"role": "user", "content": ORCH_PROMPT.replace("{QUERY}", query or "")},
            ],
            temperature=0.1,
            max_tokens=400,
        )
        raw = resp.choices[0].message.content
        plan = json.loads(raw)
        # sanity check
        assert isinstance(plan.get("plan"), list) and plan["plan"], "plan vuoto"
        for step in plan["plan"]:
            assert step["agent"] in {"analyst_news", "analyst_tech", "analyst_fund", "portfolio_mgr"}
            assert step.get("brief")
        return plan
    except Exception:
        # fallback rule-based
        return _fallback_plan(query)

def build_tasks(plan: Dict) -> List[Task]:
    name2agent = {
        "analyst_news": analyst_news,
        "analyst_tech": analyst_tech,
        "analyst_fund": analyst_fund,
        "portfolio_mgr": portfolio_mgr,
    }
    tasks: List[Task] = []
    for step in plan["plan"]:
        agent = name2agent[step["agent"]]
        tasks.append(Task(
            description=step["brief"],
            agent=agent,
            expected_output="Sintesi chiara e azionabile, cita indicatori/fonti usati e assunzioni."
        ))
    return tasks

def run_orchestration(query: str, client) -> str:
    """Crea il piano, costruisce i task, avvia CrewAI e restituisce la risposta finale."""
    plan = plan_from_llm(query=query, client=client)
    tasks = build_tasks(plan)
    crew = Crew(
        agents=[analyst_news, analyst_tech, analyst_fund, portfolio_mgr],
        tasks=tasks,
        process=Process.sequential,
        verbose=False,
    )
    result = crew.kickoff()
    # Puoi post‑processare il risultato qui se vuoi applicare tone/final_goal.
    return str(result)
