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
        response = requests.get(url)
        response.raise_for_status() 
        return "success"
    except Exception as e:
        print(f'Error fetching {url}: {e}')
        return "failure"

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
    probe_exists = False
    for probe in probes:
        probe_exists = True
        print(f"Adding probe {probe.url} with duration {probe.duration} for monitoring")
        start_monitoring_thread(probe)
    if not probe_exists:
        print("No probes exist in the database")

def start_health_check():
    monitor_existing_probes()

# Django signals to handle new probe creation and deletion
@receiver(post_save, sender=Probe)
def probe_post_save(sender, instance, created, **kwargs):
    if created:
        start_monitoring_thread(instance)

@receiver(post_delete, sender=Probe)
def probe_post_delete(sender, instance, **kwargs):
    stop_monitoring_thread(instance.pk)