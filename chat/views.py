from django.shortcuts import render
from django.http import JsonResponse
from core.rag.config import BasePrompt, RAGPrompt

# Create your views here.
def chat(request):
    return render(request, "chat.html")


async def send_question(request):
    if request.method == 'POST':
        from core import engine

        question = request.POST.get('question')
        if not question:
            return JsonResponse({'status': 'error', 'message': 'No input provided'}, status=400)
        
        try:
            answer = await engine.rag.generate(question=question, 
                                           prompt=BasePrompt.prompt)
                
            return JsonResponse({'status': 'success', 'question': question, 'answer': answer})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': "error di view send_question"}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)