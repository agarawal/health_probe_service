import time
import requests
import threading
from health_probe.models import Probe
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# Global dictionary to store currently monitored probes and their threads
monitored_probes = {}

def fetch(url):
    try:
        # Simulating a successful response for illustration
        # response = requests.get(url)
        return "success"
    except requests.RequestException as e:
        print(f'Error fetching {url}: {e}')
        return None

def monitor_probe(probe):
    while True:
        response = fetch(probe.url)
        if response:
            print(f'Health check for {probe.url}: {response}')
        time.sleep(probe.duration)

def start_monitoring_thread(probe):
    t = threading.Thread(target=monitor_probe, args=(probe,), daemon=True)
    monitored_probes[probe.pk] = t
    t.start()

def stop_monitoring_thread(probe_id):
    if probe_id in monitored_probes:
        monitored_probes[probe_id].join()  # Wait for thread to complete
        del monitored_probes[probe_id]

def monitor_existing_probes():
    probes = Probe.objects.all()
    for probe in probes:
        print(f"Monitoring probe {probe.url} with duration {probe.duration}")
        start_monitoring_thread(probe)

def start_health_check():
    monitor_existing_probes()
    # This function can potentially run forever, depending on your application's needs

# Django signals to handle new probe creation and deletion
@receiver(post_save, sender=Probe)
def probe_post_save(sender, instance, created, **kwargs):
    if created:
        start_monitoring_thread(instance)

@receiver(post_delete, sender=Probe)
def probe_post_delete(sender, instance, **kwargs):
    stop_monitoring_thread(instance.pk)

# Ensure the health check starts
start_health_check()