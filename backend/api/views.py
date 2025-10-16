from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
import json
import requests
from .prompts import (
    get_strategy_prompt,
    get_regenerate_strategy_prompt,
    get_content_prompt,
    get_trending_reels_prompt,
    get_optimize_idea_prompt
)

def call_ollama(prompt, temperature=0.7, max_tokens=2000):
    """Helper function per chiamare Ollama"""
    try:
        response = requests.post(
            f"{settings.OLLAMA_BASE_URL}/api/generate",
            json={
                'model': settings.OLLAMA_MODEL,
                'prompt': prompt,
                'stream': False,
                'options': {
                    'temperature': temperature,
                    'num_predict': max_tokens
                }
            },
            timeout=180  # 3 minuti per risposte lunghe
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get('response', '')
        else:
            raise Exception(f"Ollama returned status {response.status_code}: {response.text}")
    
    except Exception as e:
        raise Exception(f"Failed to connect to Ollama: {str(e)}")


@csrf_exempt
@require_http_methods(["GET"])
def health_check(request):
    """Endpoint per verificare che il server Django sia attivo"""
    return JsonResponse({
        'status': 'ok',
        'message': 'Django server is running',
        'ollama_url': settings.OLLAMA_BASE_URL,
        'ollama_model': settings.OLLAMA_MODEL
    })


@csrf_exempt
@require_http_methods(["POST", "GET"])
def test_ollama(request):
    """Endpoint per testare la connessione con Ollama"""
    try:
        if request.method == 'GET':
            prompt = "Say hello in Italian"
        else:
            data = json.loads(request.body)
            prompt = data.get('prompt', 'Hello, how are you?')
        
        response_text = call_ollama(prompt, max_tokens=500)
        
        return JsonResponse({
            'success': True,
            'prompt': prompt,
            'response': response_text,
            'model': settings.OLLAMA_MODEL
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'message': 'Failed to generate response.'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def generate_strategy(request):
    """Genera una strategia di contenuto completa"""
    try:
        data = json.loads(request.body)
        
        # Estrai parametri
        niche = data.get('niche', '')
        target_audience = data.get('target_audience', 'General audience')
        goals = data.get('goals', 'Increase engagement')
        posting_frequency = data.get('posting_frequency', '3-5 posts per week')
        
        if not niche:
            return JsonResponse({
                'success': False,
                'error': 'Niche is required'
            }, status=400)
        
        # Genera il prompt
        prompt = get_strategy_prompt(niche, target_audience, goals, posting_frequency)
        
        # Chiama Ollama con timeout più lungo
        response_text = call_ollama(prompt, temperature=0.8, max_tokens=4000)
        
        return JsonResponse({
            'success': True,
            'strategy': response_text,
            'metadata': {
                'niche': niche,
                'target_audience': target_audience,
                'goals': goals,
                'posting_frequency': posting_frequency
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'message': 'Failed to generate strategy.'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def regenerate_strategy(request):
    """Rigenera una strategia basandosi su feedback"""
    try:
        data = json.loads(request.body)
        
        previous_strategy = data.get('previous_strategy', '')
        feedback = data.get('feedback', '')
        
        if not previous_strategy or not feedback:
            return JsonResponse({
                'success': False,
                'error': 'Both previous_strategy and feedback are required'
            }, status=400)
        
        # Genera il prompt
        prompt = get_regenerate_strategy_prompt(previous_strategy, feedback)
        
        # Chiama Ollama
        response_text = call_ollama(prompt, temperature=0.8, max_tokens=4000)
        
        return JsonResponse({
            'success': True,
            'strategy': response_text,
            'metadata': {
                'feedback_applied': feedback
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'message': 'Failed to regenerate strategy.'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def generate_content(request):
    """Genera contenuto specifico per un post"""
    try:
        data = json.loads(request.body)
        
        topic = data.get('topic', '')
        post_type = data.get('post_type', 'post')
        tone = data.get('tone', 'professional')
        target_audience = data.get('target_audience', 'General audience')
        
        if not topic:
            return JsonResponse({
                'success': False,
                'error': 'Topic is required'
            }, status=400)
        
        # Genera il prompt
        prompt = get_content_prompt(topic, post_type, tone, target_audience)
        
        # Chiama Ollama
        response_text = call_ollama(prompt, temperature=0.7, max_tokens=1500)
        
        return JsonResponse({
            'success': True,
            'content': response_text,
            'metadata': {
                'topic': topic,
                'post_type': post_type,
                'tone': tone
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'message': 'Failed to generate content.'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def generate_trending_reels(request):
    """Genera idee per reels trending"""
    try:
        data = json.loads(request.body)
        
        niche = data.get('niche', '')
        target_audience = data.get('target_audience', 'General audience')
        
        if not niche:
            return JsonResponse({
                'success': False,
                'error': 'Niche is required'
            }, status=400)
        
        # Genera il prompt
        prompt = get_trending_reels_prompt(niche, target_audience)
        
        # Chiama Ollama
        response_text = call_ollama(prompt, temperature=0.9, max_tokens=3000)
        
        return JsonResponse({
            'success': True,
            'ideas': response_text,
            'metadata': {
                'niche': niche,
                'target_audience': target_audience
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'message': 'Failed to generate trending reels ideas.'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def optimize_idea(request):
    """Ottimizza un'idea esistente"""
    try:
        data = json.loads(request.body)
        
        idea_content = data.get('idea_content', '')
        optimization_goal = data.get('optimization_goal', 'engagement')
        
        if not idea_content:
            return JsonResponse({
                'success': False,
                'error': 'idea_content is required'
            }, status=400)
        
        # Genera il prompt
        prompt = get_optimize_idea_prompt(idea_content, optimization_goal)
        
        # Chiama Ollama
        response_text = call_ollama(prompt, temperature=0.7, max_tokens=2000)
        
        return JsonResponse({
            'success': True,
            'optimized_idea': response_text,
            'metadata': {
                'optimization_goal': optimization_goal
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'message': 'Failed to optimize idea.'
        }, status=500)