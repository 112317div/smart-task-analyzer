"""
Priority Scoring Algorithm for Task Analysis
"""

from datetime import datetime, date
from typing import List, Dict, Any, Tuple


class TaskPriorityScorer:
    """
    Calculates priority scores for tasks based on multiple weighted factors.
    """
    
    URGENCY_MAX = 40
    IMPORTANCE_MAX = 30
    EFFORT_MAX = 15
    DEPENDENCY_MAX = 15
    
    STRATEGIES = {
        'smart': {
            'urgency': 1.0,
            'importance': 1.0,
            'effort': 1.0,
            'dependency': 1.0
        },
        'fastest': {
            'urgency': 0.5,
            'importance': 0.5,
            'effort': 4.0,
            'dependency': 0.5
        },
        'impact': {
            'urgency': 0.3,
            'importance': 3.0,
            'effort': 0.2,
            'dependency': 1.5
        },
        'deadline': {
            'urgency': 3.0,
            'importance': 0.8,
            'effort': 0.5,
            'dependency': 0.7
        }
    }
    
    def __init__(self, strategy: str = 'smart'):
        if strategy not in self.STRATEGIES:
            raise ValueError(f"Invalid strategy. Choose from: {list(self.STRATEGIES.keys())}")
        self.strategy = strategy
        self.multipliers = self.STRATEGIES[strategy]
    
    def calculate_urgency_score(self, due_date: date, current_date: date = None) -> Tuple[float, str]:
        if current_date is None:
            current_date = date.today()
        
        days_until_due = (due_date - current_date).days
        
        if days_until_due < 0:
            return self.URGENCY_MAX, f"Overdue by {abs(days_until_due)} day(s)"
        elif days_until_due == 0:
            return 35, "Due today"
        elif days_until_due == 1:
            return 35, "Due tomorrow"
        elif days_until_due <= 3:
            return 30, "Due within 3 days"
        elif days_until_due <= 7:
            return 20, "Due this week"
        elif days_until_due <= 14:
            return 10, "Due within 2 weeks"
        else:
            return 5, f"Due in {days_until_due} days"
    
    def calculate_importance_score(self, importance: int) -> Tuple[float, str]:
        if not 1 <= importance <= 10:
            importance = max(1, min(10, importance))
        
        score = (importance / 10) * self.IMPORTANCE_MAX
        
        if importance >= 8:
            explanation = "High importance"
        elif importance >= 6:
            explanation = "Medium importance"
        else:
            explanation = "Lower importance"
        
        return score, explanation
    
    def calculate_effort_score(self, estimated_hours: float) -> Tuple[float, str]:
        if estimated_hours <= 1:
            return self.EFFORT_MAX, "Quick win (≤1 hour)"
        elif estimated_hours <= 3:
            return 10, "Short task (1-3 hours)"
        elif estimated_hours <= 8:
            return 5, "Medium task (3-8 hours)"
        else:
            return 2, f"Large task ({estimated_hours} hours)"
    
    def calculate_dependency_score(self, task_id: str, all_tasks: List[Dict]) -> Tuple[float, str]:
        blocking_count = sum(
            1 for task in all_tasks
            if task_id in task.get('dependencies', [])
        )
        
        if blocking_count == 0:
            return 0, "No tasks blocked"
        
        score = min(self.DEPENDENCY_MAX, blocking_count * 5)
        explanation = f"Blocks {blocking_count} task(s)"
        
        return score, explanation
    
    def detect_circular_dependencies(self, tasks: List[Dict]) -> bool:
        def has_cycle(task_id: str, visited: set, rec_stack: set) -> bool:
            visited.add(task_id)
            rec_stack.add(task_id)
            
            task = next((t for t in tasks if str(t.get('id')) == str(task_id)), None)
            if task and 'dependencies' in task:
                for dep_id in task['dependencies']:
                    dep_id_str = str(dep_id)
                    if dep_id_str not in visited:
                        if has_cycle(dep_id_str, visited, rec_stack):
                            return True
                    elif dep_id_str in rec_stack:
                        return True
            
            rec_stack.remove(task_id)
            return False
        
        visited = set()
        for task in tasks:
            task_id = str(task.get('id'))
            if task_id not in visited:
                if has_cycle(task_id, visited, set()):
                    return True
        
        return False
    
    def calculate_priority(self, task: Dict, all_tasks: List[Dict]) -> Dict[str, Any]:
        task_id = str(task.get('id', ''))
        
        due_date_str = task.get('due_date')
        if isinstance(due_date_str, str):
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        elif isinstance(due_date_str, date):
            due_date = due_date_str
        else:
            due_date = date.today()
        
        urgency_score, urgency_exp = self.calculate_urgency_score(due_date)
        importance_score, importance_exp = self.calculate_importance_score(
            task.get('importance', 5)
        )
        effort_score, effort_exp = self.calculate_effort_score(
            task.get('estimated_hours', 1)
        )
        dependency_score, dependency_exp = self.calculate_dependency_score(
            task_id, all_tasks
        )
        
        weighted_urgency = urgency_score * self.multipliers['urgency']
        weighted_importance = importance_score * self.multipliers['importance']
        weighted_effort = effort_score * self.multipliers['effort']
        weighted_dependency = dependency_score * self.multipliers['dependency']
        
        total_score = (
            weighted_urgency + 
            weighted_importance + 
            weighted_effort + 
            weighted_dependency
        )
        
        explanations = []
        if urgency_exp:
            explanations.append(urgency_exp)
        if importance_exp and task.get('importance', 5) >= 7:
            explanations.append(importance_exp)
        if effort_exp and task.get('estimated_hours', 1) <= 2:
            explanations.append(effort_exp)
        if dependency_exp and dependency_score > 0:
            explanations.append(dependency_exp)
        
        explanation = ' • '.join(explanations) if explanations else 'Standard priority'
        
        if total_score >= 70:
            priority_level = 'Critical'
        elif total_score >= 50:
            priority_level = 'High'
        elif total_score >= 30:
            priority_level = 'Medium'
        else:
            priority_level = 'Low'
        
        return {
            'score': round(total_score, 1),
            'priority_level': priority_level,
            'explanation': explanation,
            'breakdown': {
                'urgency': round(weighted_urgency, 1),
                'importance': round(weighted_importance, 1),
                'effort': round(weighted_effort, 1),
                'dependency': round(weighted_dependency, 1)
            }
        }
    
    def score_and_sort_tasks(self, tasks: List[Dict]) -> List[Dict]:
        has_circular = self.detect_circular_dependencies(tasks)
        
        scored_tasks = []
        for task in tasks:
            score_data = self.calculate_priority(task, tasks)
            scored_task = {**task, **score_data}
            if has_circular:
                scored_task['warning'] = 'Circular dependencies detected'
            scored_tasks.append(scored_task)
        
        scored_tasks.sort(key=lambda x: x['score'], reverse=True)
        
        return scored_tasks
    
    def get_top_suggestions(self, tasks: List[Dict], count: int = 3) -> List[Dict]:
        scored_tasks = self.score_and_sort_tasks(tasks)
        suggestions = []
        
        for rank, task in enumerate(scored_tasks[:count], 1):
            recommendation = self._generate_recommendation(task, rank)
            suggestions.append({
                'task': task,
                'rank': rank,
                'recommendation': recommendation
            })
        
        return suggestions
    
    def _generate_recommendation(self, task: Dict, rank: int) -> str:
        recommendations = []
        
        if rank == 1:
            recommendations.append("This should be your top priority.")
        
        score = task.get('score', 0)
        if score >= 70:
            recommendations.append("This is a critical task that needs immediate attention.")
        elif score >= 50:
            recommendations.append("This is a high-priority task you should tackle soon.")
        
        breakdown = task.get('breakdown', {})
        if breakdown.get('urgency', 0) > 30:
            recommendations.append("Time is running out - address this ASAP.")
        
        if breakdown.get('effort', 0) > 10:
            recommendations.append("This is a quick win that can build momentum.")
        
        if breakdown.get('dependency', 0) > 0:
            recommendations.append("Completing this will unblock other tasks.")
        
        return ' '.join(recommendations) if recommendations else "Work on this when you have time."