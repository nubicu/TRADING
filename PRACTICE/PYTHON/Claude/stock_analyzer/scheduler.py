"""
Scheduler pentru update-uri automate
Update-uri: 
- 6:30 AM EST (3h înainte NYSE open)
- 10:30 AM EST (1h după NYSE open)
"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import pytz
import requests
import time

class StockUpdateScheduler:
    """Scheduler pentru update-uri automate"""
    
    def __init__(self, app_url='http://localhost:5000'):
        self.app_url = app_url
        self.scheduler = BackgroundScheduler()
        self.est_tz = pytz.timezone('America/New_York')
        
    def start(self):
        """Pornește scheduler-ul cu task-uri programate"""
        print("🕐 Starting Stock Update Scheduler...")
        print(f"📍 Timezone: {self.est_tz}")
        print(f"🔗 App URL: {self.app_url}")
        
        # Task 1: Pre-market update - 6:30 AM EST (3h înainte de deschidere)
        self.scheduler.add_job(
            func=self.pre_market_update,
            trigger=CronTrigger(
                hour=6,
                minute=30,
                timezone=self.est_tz
            ),
            id='pre_market_update',
            name='Pre-Market Update (6:30 AM EST)',
            replace_existing=True
        )
        
        # Task 2: Post-open update - 10:30 AM EST (1h după deschidere)
        self.scheduler.add_job(
            func=self.post_open_update,
            trigger=CronTrigger(
                hour=10,
                minute=30,
                timezone=self.est_tz
            ),
            id='post_open_update',
            name='Post-Open Update (10:30 AM EST)',
            replace_existing=True
        )
        
        # Task pentru testare: update la fiecare 30 minute (opțional - comentează în producție)
        # self.scheduler.add_job(
        #     func=self.manual_update,
        #     trigger='interval',
        #     minutes=30,
        #     id='test_update',
        #     name='Test Update (every 30 min)'
        # )
        
        self.scheduler.start()
        
        # Afișează task-uri programate
        self._print_scheduled_jobs()
        
        print("\n✅ Scheduler started successfully!")
        print("💡 Press Ctrl+C to stop\n")
        
    def pre_market_update(self):
        """Update pre-market - 6:30 AM EST"""
        self._trigger_update('pre_market')
    
    def post_open_update(self):
        """Update post-open - 10:30 AM EST"""
        self._trigger_update('post_open')
    
    def manual_update(self):
        """Update manual pentru testare"""
        self._trigger_update('manual')
    
    def _trigger_update(self, update_type):
        """Trigger update către Flask app"""
        try:
            now_est = datetime.now(self.est_tz)
            print(f"\n{'='*60}")
            print(f"🔄 Triggering {update_type} update")
            print(f"⏰ Time: {now_est.strftime('%Y-%m-%d %H:%M:%S %Z')}")
            print(f"{'='*60}\n")
            
            # Call Flask API endpoint
            response = requests.post(
                f'{self.app_url}/api/update',
                json={'update_type': update_type},
                timeout=300  # 5 minute timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Update completed successfully!")
                print(f"📊 Stocks updated: {result.get('updated_stocks', 0)}")
                print(f"⏱️  Duration: {result.get('duration', 0):.2f} seconds")
            else:
                print(f"❌ Update failed with status code: {response.status_code}")
                print(f"Response: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ Cannot connect to Flask app at {self.app_url}")
            print("   Make sure app.py is running!")
        except Exception as e:
            print(f"❌ Error during update: {str(e)}")
    
    def _print_scheduled_jobs(self):
        """Afișează toate task-urile programate"""
        print("\n📅 Scheduled Jobs:")
        print("-" * 60)
        
        jobs = self.scheduler.get_jobs()
        if not jobs:
            print("No jobs scheduled")
            return
        
        for job in jobs:
            print(f"\n🔹 {job.name}")
            print(f"   ID: {job.id}")
            print(f"   Next run: {job.next_run_time}")
            
        print("-" * 60)
    
    def stop(self):
        """Oprește scheduler-ul"""
        print("\n🛑 Stopping scheduler...")
        self.scheduler.shutdown()
        print("✅ Scheduler stopped")


def main():
    """Main function pentru rulare standalone"""
    import signal
    import sys
    
    scheduler = StockUpdateScheduler()
    
    def signal_handler(sig, frame):
        print('\n\n📌 Interrupt received...')
        scheduler.stop()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    scheduler.start()
    
    # Keep running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        scheduler.stop()


if __name__ == '__main__':
    main()
