# orchestrator.py
from crewai import Task, Crew, Process
from agents import analyst_news, analyst_tech, analyst_fund, portfolio_mgr
from typing import List, Dict

def plan_from_llm(query: str) -> Dict:
    # QUI usi OpenAI per produrre il piano con il prompt Orchestrator
    # (riusa il tuo client OpenAI)
    # ritorna dict con "plan": [{"agent":"analyst_tech","brief":"..."} ...]
    ...

def build_tasks(plan: Dict) -> List[Task]:
    tasks = []
    for step in plan["plan"]:
        agent = {
            "analyst_news": analyst_news,
            "analyst_tech": analyst_tech,
            "analyst_fund": analyst_fund,
            "portfolio_mgr": portfolio_mgr,
        }[step["agent"]]
        tasks.append(Task(
            description=step["brief"],
            agent=agent,
            expected_output="Sintesi chiara e azionabile, con fonti/indicatori usati."
        ))
    return tasks

def run_orchestration(query: str) -> str:
    plan = plan_from_llm(query)
    tasks = build_tasks(plan)
    crew = Crew(
        agents=[analyst_news, analyst_tech, analyst_fund, portfolio_mgr],
        tasks=tasks,
        process=Process.sequential  # o hierarchical, come preferisci
    )
    result = crew.kickoff()
    # opzionale: prompt finale che “assembla” i pezzi in un’unica risposta
    return str(result)
