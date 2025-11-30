from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Task
from .serializers import TaskSerializer, TaskAnalysisInputSerializer
from .scoring import TaskPriorityScorer


class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Task CRUD operations.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


@api_view(['POST'])
def analyze_tasks(request):
    """
    POST /api/tasks/analyze/
    Analyze and sort tasks by priority score.
    """
    input_serializer = TaskAnalysisInputSerializer(data=request.data)
    
    if not input_serializer.is_valid():
        return Response(
            {
                'error': 'Invalid input data',
                'details': input_serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    tasks = input_serializer.validated_data['tasks']
    strategy = input_serializer.validated_data.get('strategy', 'smart')
    
    for idx, task in enumerate(tasks):
        if 'id' not in task:
            task['id'] = f"task_{idx + 1}"
    
    try:
        scorer = TaskPriorityScorer(strategy=strategy)
        scored_tasks = scorer.score_and_sort_tasks(tasks)
        has_circular = scorer.detect_circular_dependencies(tasks)
        
        return Response({
            'tasks': scored_tasks,
            'strategy_used': strategy,
            'total_tasks': len(scored_tasks),
            'circular_dependencies': has_circular,
            'message': 'Tasks analyzed successfully'
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response(
            {
                'error': 'Error analyzing tasks',
                'details': str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def suggest_tasks(request):
    """
    POST /api/tasks/suggest/
    Get top 3 task suggestions with explanations.
    """
    input_serializer = TaskAnalysisInputSerializer(data=request.data)
    
    if not input_serializer.is_valid():
        return Response(
            {
                'error': 'Invalid input data',
                'details': input_serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    tasks = input_serializer.validated_data['tasks']
    strategy = input_serializer.validated_data.get('strategy', 'smart')
    count = request.data.get('count', 3)
    
    for idx, task in enumerate(tasks):
        if 'id' not in task:
            task['id'] = f"task_{idx + 1}"
    
    try:
        scorer = TaskPriorityScorer(strategy=strategy)
        suggestions = scorer.get_top_suggestions(tasks, count=count)
        
        return Response({
            'suggestions': suggestions,
            'strategy_used': strategy,
            'message': f'Top {len(suggestions)} task suggestions generated'
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response(
            {
                'error': 'Error generating suggestions',
                'details': str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def health_check(request):
    """
    GET /api/health/
    Simple health check endpoint.
    """
    return Response({
        'status': 'healthy',
        'message': 'Task Analyzer API is running'
    }, status=status.HTTP_200_OK)


class TaskAnalysisView(APIView):
    """
    Class-based view for task analysis with additional features.
    """
    
    def post(self, request):
        return analyze_tasks(request)
    
    def get(self, request):
        strategies = {
            'smart': {
                'name': 'Smart Balance',
                'description': 'Balanced approach considering all factors equally',
                'best_for': 'General task prioritization'
            },
            'fastest': {
                'name': 'Fastest Wins',
                'description': 'Prioritizes quick, low-effort tasks for momentum',
                'best_for': 'When you need quick progress and motivation'
            },
            'impact': {
                'name': 'High Impact',
                'description': 'Focuses on importance and blocking tasks',
                'best_for': 'When you want to maximize value delivered'
            },
            'deadline': {
                'name': 'Deadline Driven',
                'description': 'Emphasizes urgency and time-sensitive tasks',
                'best_for': 'When you have tight deadlines to meet'
            }
        }
        
        return Response({
            'strategies': strategies,
            'default': 'smart',
            'message': 'Available sorting strategies'
        }, status=status.HTTP_200_OK)