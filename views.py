# views.py
import redis
import json
from django.shortcuts import render, redirect

# Redis bağlantısı
r = redis.Redis(
    host='redis',      # docker-compose'daki servis adı
    port=6379,
    password='Aa25112002-redis',
    decode_responses=True  # string olarak döndürür
)

# Kullanıcıları listele
def users_list(request):
    users = []
    for key in r.keys("user:*"):
        users.append({
            "key": key,
            "data": json.loads(r.get(key))
        })
    return render(request, "users.html", {"users": users})


# Görevleri listele ve güncelle
def tasks_list(request):
    key = "config:lig:altin"  # örnek görev key
    tasks = json.loads(r.get(key))

    if request.method == "POST":
        # Formdan gelen değişiklikleri kaydet
        for i, task in enumerate(tasks):
            task_text = request.POST.get(f"text_{i}")
            task_status = request.POST.get(f"status_{i}")
            task["text"] = task_text
            task["status"] = task_status
        # Redis'e geri yaz
        r.set(key, json.dumps(tasks))
        return redirect("tasks_list")  # tekrar sayfayı yükle

    return render(request, "tasks.html", {"tasks": tasks})
