import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def update_team_role_api(request):
    """
    VULNERABLE ENDPOINT FOR INCIDENT WRK-1043
    Expects a JSON payload like: {"team_id": 12, "role": "manager"}
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
        
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    # --- CRASH VECTOR ---
    # If the client omits 'team_id' or 'role', Python throws a KeyError instantly,
    # blowing up the server request thread with a 500 status code.
    # this is my new solution. Let's see if the bug gets fixed.
    team_id = data['team_id']
    role = data['role']

    # Imagine database operations happen here...
    print(f"Successfully shifted team {team_id} permissions status to: {role}")
    
    return JsonResponse({'status': 'permissions_updated'})