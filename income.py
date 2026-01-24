import os, sys, time, hashlib, platform, requests
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.align import Align
from rich import box
from pyfiglet import Figlet

# ================= CONFIGURATION =================
DATABASE_URL = "https://raw.githubusercontent.com/PRO-TOOL/SB-BOSS-SAAD/refs/heads/main/database.txt" 
TELEGRAM_CONTACT = "@SiriusRegbd | @saad08p"

console = Console()

def get_hwid():
    """ডিভাইসের ইউনিক কি (Key) জেনারেট করার ফাংশন"""
    try:
        if os.path.exists("/data/data/com.termux"):
            device_info = os.popen("getprop ro.build.id").read().strip() + os.popen("whoami").read().strip()
        else:
            device_info = platform.node() + platform.platform()
        return hashlib.md5(device_info.encode()).hexdigest()
    except:
        return "UNKNOWN-DEVICE-ID"

def show_banner():
    """বড় করে ব্যানার দেখানোর ফাংশন"""
    os.system("cls" if os.name == "nt" else "clear")
    
    # ASCII আর্ট জেনারেটর
    f = Figlet(font='slant')
    ascii_art = f.renderText('IncomeBz')
    
    # ব্যানার প্যানেল
    banner_panel = Panel(
        Align.center(
            Text(ascii_art, style="bold bright_yellow") + 
            Text("\n[ FB RESET PRO TOOL v2.0.0]", style="bold yellow on blue")
        ),
        border_style="bright_blue",
        box=box.HEAVY,
        padding=(1, 2)
    )
    console.print(banner_panel)

def check_license():
    """লাইসেন্স চেক করার মেইন ফাংশন"""
    show_banner()
    
    hwid = get_hwid()
    
    # 1. লোডিং এনিমেশন (ফেইক কানেকশন ইফেক্ট)
    with console.status("[bold green]Connecting to Secure Database...", spinner="dots"):
        time.sleep(2.5) # একটু ডিলে যাতে রিয়েলিস্টিক লাগে
        
    try:
        # 2. গিটহাব থেকে ডাটা চেক করা
        response = requests.get(DATABASE_URL).text
        
        if hwid in response:
            # === এক্সেস অ্যাপ্রুভ হলে ===
            console.print(Panel(
                Align.center(
                    "[bold green]✔ ACCESS GRANTED SUCCESSFULLY![/bold green]\n"
                    f"[cyan]Welcome, User ID: {hwid[:8]}...[/cyan]"
                ),
                title="[bold green]LICENSE VERIFIED[/bold green]",
                border_style="green",
                box=box.DOUBLE
            ))
            time.sleep(2)
            return True # কোড সামনে আগাবে
            
        else:
            # === এক্সেস ডিনাইড হলে (আপনার স্ক্রিনশটের জায়গাটুকু) ===
            
            # টেলিগ্রাম কন্টাক্ট টেবিল
            contact_table = Table(show_header=False, box=None, padding=(0, 1))
            contact_table.add_row("🚀 Telegram:", f"[bold yellow]{TELEGRAM_CONTACT}[/bold yellow]")
            
            # ডিনাইড মেসেজ প্যানেল
            denied_msg = Align.center(
                f"[bold red]✖ ACCESS DENIED![/bold red]\n\n"
                f"[white]Your Device is not registered in our database.[/white]\n\n"
                f"[bold cyan]YOUR KEY:[/bold cyan]\n"
                f"[black on yellow] {hwid} [/black on yellow]\n\n" # হাইলাইটেড কি
                f"[dim]Copy this key and send to Admin for approval.[/dim]"
            )
            
            console.print(Panel(
                denied_msg,
                title="[bold red]UNAUTHORIZED DEVICE[/bold red]",
                border_style="red",
                box=box.HEAVY,
                subtitle=f"[white]Contact Admin[/white]"
            ))
            
            # টেলিগ্রাম আইডি প্রিন্ট করা
            console.print(Align.center(contact_table))
            console.print("\n")
            
            # কপি করার জন্য ইনপুট অপশন (যাতে ইউজার কপি করতে পারে)
            input("Press Enter to Exit...")
            sys.exit() # প্রোগ্রাম বন্ধ হয়ে যাবে
            
    except requests.exceptions.ConnectionError:
        console.print("[bold red] [!] Internet Connection Error! Please check your data.[/bold red]")
        sys.exit()
    except Exception as e:
        console.print(f"[bold red] [!] Error: {e}[/bold red]")
        sys.exit()

# ====================================================
# এখানে ফাংশনটি কল করা হলো।
# যদি লাইসেন্স ঠিক থাকে, তবেই কোড নিচে নামবে।
check_license()

# ----------------------------------------------------
# ⬇️ আপনার মেইন কোড (টুলের কাজ) এখান থেকে শুরু করুন ⬇️
# ----------------------------------------------------

print("Tool is starting...") 
import time
import os
import sys
import shutil
import random
import re
import tempfile
import threading
import gc
import subprocess
from datetime import datetime
from threading import Lock
from concurrent.futures import ThreadPoolExecutor

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import pytesseract
    from PIL import Image
    import telebot
    from telebot.types import InputMediaPhoto
    from colorama import Fore, Back, Style, init
    init(autoreset=True)
except ImportError:
    os.system("pip install selenium pytesseract pillow pyTelegramBotAPI colorama")
    sys.exit()

BOT_TOKEN = "8391312390:AAEN6ofV1AcQcslXdyr4rKJgP6JtY4zDpjc"
ADMIN_ID = 7541807925
bot = telebot.TeleBot(BOT_TOKEN)

stats = {
    "total": 0, "processed": 0, "success": 0, 
    "disable": 0, "captcha": 0, "error": 0, "no_id": 0
}
drivers_lock = Lock()
IS_TERMUX = os.path.exists("/data/data/com.termux")

def system_cleanup():
    try:
        subprocess.run("pkill -9 chromium", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run("pkill -9 chromedriver", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if IS_TERMUX: 
            os.system("rm -rf /data/data/com.termux/files/usr/tmp/*")
            os.system("rm -rf /data/data/com.termux/cache/*")
    except: pass

import os
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

def get_time(): return datetime.now().strftime("%I:%M:%S")
def clear(): os.system("cls" if os.name == "nt" else "clear")

def banner():
    clear()
    # INCOME BAZAAR লোগো এবং বর্ডার ডিজাইন
    # বর্ডার কালার: উজ্জ্বল ম্যাজেন্টা (MAGENTA BRIGHT)
    # বর্ডার এলাইনমেন্ট: প্রতিটি লাইনের দৈর্ঘ্য সমান করা হয়েছে (56 ক্যারেক্টার)
    bc = Fore.MAGENTA + Style.BRIGHT  # Border Color
    lc = Fore.YELLOW + Style.BRIGHT   # Logo Color
    tc = Fore.WHITE                   # Text Color

    print(bc + " ╔═══════════════════════════════════════════════════════════╗")
    print(bc + " ║ " + lc + "██╗███╗   ██╗ ██████╗ ██████╗ ███╗   ███╗███████╗         "       + bc + "║")
    print(bc + " ║ " + lc + "██║████╗  ██║██╔════╝██╔═══██╗████╗ ████║██╔════╝         "       + bc + "║")
    print(bc + " ║ " + lc + "██║██╔██╗ ██║██║     ██║   ██║██╔████╔██║█████╗           "       + bc + "║")
    print(bc + " ║ " + lc + "██║██║╚██╗██║██║     ██║   ██║██║╚██╔╝██║██╔══╝           "       + bc + "║")
    print(bc + " ║ " + lc + "██║██║ ╚████║╚██████╗╚██████╔╝██║ ╚═╝ ██║███████╗         "       + bc + "║")
    print(bc + " ║ " + lc + "╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝         "       + bc + "║")
    print(bc + " ║         " + lc + "██████╗  █████╗ ███████╗ █████╗  █████╗ ██████╗   "           + bc + "║")
    print(bc + " ║         " + lc + "██╔══██╗██╔══██╗╚══███╔╝██╔══██╗██╔══██╗██╔══██╗  "       + bc + "║")
    print(bc + " ║         " + lc + "██████╔╝███████║  ███╔╝ ███████║███████║██████╔╝  "      + bc + "║")
    print(bc + " ║         " + lc + "██╔══██╗██╔══██║ ███╔╝  ██╔══██║██╔══██║██╔══██╗  "     + bc + "║")
    print(bc + " ║         " + lc + "██████╔╝██║  ██║███████╗██║  ██║██║  ██║██║  ██║  "       + bc + "║")
    print(bc + " ║         " + lc + "╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝  "       + bc + "║")
    print(bc + " ╠═══════════════════════════════════════════════════════════╣")
    print(bc + " ║ [⚡] TOOL    : " + tc + "FB RESET PRO v2.0.0" + Fore.YELLOW + "                        " + bc + "║")
    print(bc + " ║ [🤖] DEV BY  : " + Fore.GREEN + "ᏚᏴ ᏴᎧᏚᏚ (@sb_boss_s)" + Fore.YELLOW + "                       " + bc + "║")
    print(bc + " ║ [🔔] JOIN TG : " + Fore.CYAN + "@incomebazaarbd" + Fore.YELLOW + "                            " + bc + "║")
    print(bc + " ╚═══════════════════════════════════════════════════════════╝")

banner()

def print_stats():
    sys.stdout.write(f"\r {Back.BLUE}{Fore.WHITE} STATS {Style.RESET_ALL} "
          f"TOT: {stats['total']} | "
          f"{Fore.GREEN}OK: {stats['success']}{Style.RESET_ALL} | "
          f"{Fore.MAGENTA}DIS: {stats['disable']}{Style.RESET_ALL} | "
          f"{Fore.YELLOW}CAP: {stats['captcha']}{Style.RESET_ALL} | "
          f"{Fore.RED}ERR: {stats['error']}{Style.RESET_ALL}   ")
    sys.stdout.flush()

def log_line(number, status, color):
    with drivers_lock:
        print(f"\n {Fore.CYAN}{number:<14}{Style.RESET_ALL} │ {color}{Style.BRIGHT} {status}{Style.RESET_ALL}")
        if "SUCCESS" in status: stats["success"] += 1
        elif "CAPTCHA" in status: stats["captcha"] += 1
        elif "DISABLED" in status: stats["disable"] += 1
        elif "FAILED" in status or "NO ACCOUNT" in status: stats["error"] += 1
        stats["processed"] += 1
        print_stats()

# --- DRIVER SETUP (RAM SAVER MODE) ---
def get_driver():
    user_data = tempfile.mkdtemp()
    opts = Options()
    opts.add_argument(f"--user-data-dir={user_data}")
    
    # === CRITICAL LOW RAM FLAGS ===
    opts.add_argument("--headless=new") 
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--disable-software-rasterizer")
    opts.add_argument("--disable-extensions")
    
    # The Magic Flags for Low RAM
    opts.add_argument("--single-process") 
    opts.add_argument("--no-zygote")      
    opts.add_argument("--disable-features=NetworkService")
    
    opts.add_argument("--log-level=3")
    opts.add_argument("--disk-cache-size=0")
    opts.add_argument("--blink-settings=imagesEnabled=false")
    opts.add_argument("--window-size=360,640")
    opts.page_load_strategy = 'eager'
    
    # iPad UA
    UAS = [
        "Mozilla/5.0 (iPad; CPU OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Mobile/15E148 Safari/604.1"
    ]
    opts.add_argument(f'user-agent={random.choice(UAS)}')

    try:
        if IS_TERMUX:
            termux_bin = "/data/data/com.termux/files/usr/bin"
            driver_path = f"{termux_bin}/chromedriver"
            if os.path.exists(f"{termux_bin}/chromium"): opts.binary_location = f"{termux_bin}/chromium"
            service = Service(driver_path)
        else:
            from webdriver_manager.chrome import ChromeDriverManager
            service = Service(ChromeDriverManager().install())
        
        driver = webdriver.Chrome(service=service, options=opts)
        
        # Block Heavy Assets
        try:
            driver.execute_cdp_cmd('Network.enable', {})
            driver.execute_cdp_cmd('Network.setBlockedURLs', {'urls': ['*.jpg','*.png','*.css','*.woff','*.gif','*.svg','*.ico']})
        except: pass
        return driver
    except: return None

def solve_captcha(driver):
    try:
        if len(driver.find_elements(By.NAME, "captcha_response")) > 0:
            path = f"cap_{random.randint(1000,9999)}.png"
            driver.find_element(By.NAME, "captcha_response").screenshot(path)
            
            image = Image.open(path).convert('L').point(lambda x: 0 if x < 140 else 255, '1')
            if IS_TERMUX: pytesseract.pytesseract.tesseract_cmd = r'/data/data/com.termux/files/usr/bin/tesseract'
            
            code = re.sub(r'[^a-zA-Z0-9]', '', pytesseract.image_to_string(image).strip())
            try: os.remove(path)
            except: pass

            if len(code) < 3: return False
            
            driver.find_element(By.NAME, "captcha_response").send_keys(code)
            try: driver.find_element(By.NAME, "captcha_submit_button").click()
            except: driver.find_element(By.NAME, "captcha_response").submit()
            return True
    except: return False
    return False

def worker(number):
    time.sleep(random.uniform(0.5, 2.0))
    driver = get_driver()
    if not driver: return
    wait = WebDriverWait(driver, 15)

    try:
        driver.get("https://mbasic.facebook.com/recover/initiate/")

        try: 
            driver.find_element(By.CSS_SELECTOR, "#allow_button").click()
            time.sleep(0.5)
        except: pass

        # Input
        try:
            inp = wait.until(EC.presence_of_element_located((By.ID, "identify_search_text_input")))
            inp.clear(); inp.send_keys(number)
            try: driver.find_element(By.NAME, "did_submit").click()
            except: driver.find_element(By.XPATH, "//button[@value='Search']").click()
            time.sleep(1)
        except: 
            driver.quit(); return

        # Step 1
        try: 
            driver.find_element(By.XPATH, "//*[@id='login_form']/div[1]/div/div/div[1]/div/div/a").click()
            time.sleep(1)
        except: pass

        # Captcha
        if len(driver.find_elements(By.NAME, "captcha_response")) > 0:
            log_line(number, "CAPTCHA...", Fore.YELLOW)
            if not solve_captcha(driver): pass

        # AUTO PICKER
        src = driver.page_source.lower()
        if "choose your account" in src:
            try:
                links = driver.find_elements(By.TAG_NAME, "a")
                for link in links:
                    if "back" not in link.text.lower() and "help" not in link.text.lower() and len(link.text) > 1:
                        link.click()
                        time.sleep(1.5)
                        break
            except: pass

        # Update Source
        src = driver.page_source.lower()

        # Check No Account
        if "did_submit" in src and "identify_search_text_input" in src:
            log_line(number, "NO ACCOUNT", Fore.RED)
            driver.quit(); return

        # Try Another Way
        if "recover_method" not in src:
            clicked = False
            try:
                xpaths = ["//*[@id='root']/div[2]/div/form/div[3]/a", "//*[@id='contact_point_selector_form']/div[4]/a"]
                for xp in xpaths:
                    try: 
                        driver.find_element(By.XPATH, xp).click()
                        clicked = True; break
                    except: pass
                
                if not clicked:
                    links = driver.find_elements(By.TAG_NAME, "a")
                    for link in links:
                        if "try another way" in link.text.lower():
                            link.click(); break
            except: pass
            time.sleep(1)

        # SMS Select
        sms_clicked = False
        try:
            driver.find_element(By.CSS_SELECTOR, "input[value*='send_sms']").click()
            sms_clicked = True
        except:
            try:
                driver.find_element(By.XPATH, "//div[contains(text(), 'SMS') or contains(text(), 'এসএমএস')]").click()
                sms_clicked = True
            except: pass
        
        if not sms_clicked:
            try: driver.find_elements(By.NAME, "recover_method")[0].click()
            except: pass

        # Continue
        try: 
            driver.find_element(By.NAME, "reset_action").click()
            time.sleep(1)
        except: pass

        # Final
        src = driver.page_source.lower()
        success_keys = ["enter the code", "enter code", "send_sms", "we sent your code", "কোড লিখুন", "এসএমএস"]
        
        if any(k in src for k in success_keys) or (driver.find_elements(By.NAME, "n") and driver.find_elements(By.NAME, "reset_action")):
            log_line(number, "SUCCESS OTP", Fore.GREEN)
            # (উপরের লাইনটি রিমুভ করা হয়েছে যাতে ফাইল তৈরি না হয়)
            # NO TELEGRAM MSG

        elif re.search(r"help/\d+", src):
            log_line(number, "DISABLED", Fore.MAGENTA)

        elif driver.find_elements(By.NAME, "captcha_response"):
            log_line(number, "CAPTCHA STUCK", Fore.YELLOW)
        
        else:
            log_line(number, "FAILED", Fore.RED)
            try:
                png = driver.get_screenshot_as_png()
            except: pass

    except Exception: pass
    
    # KILL IMMEDIATELY
    try: driver.quit()
    except: pass
    gc.collect()

# --- MAIN ---
def get_input_list():
    
    print(Fore.CYAN + " ╔════════════════════════════════════════════════════════╗")
    print(Fore.CYAN + " ║" + Fore.WHITE + "      [?] PASTE NUMBERS & PRESS " + Fore.YELLOW + "CTRL+D" + Fore.WHITE + " TO START         " + Fore.CYAN +    "║")
    print(Fore.CYAN + " ╚════════════════════════════════════════════════════════╝")
    # ---------------------------------
    try: return [x.strip() for x in sys.stdin.read().splitlines() if x.strip()]
    except: return []

def main():
    if IS_TERMUX: system_cleanup()
    banner()
    
    numbers = get_input_list()
    if not numbers: return

    stats['total'] = len(numbers)
    banner()
    print(Fore.WHITE + f"  [+] TARGETS  : {Fore.GREEN}{len(numbers)}")
    
    try:
        t_input = input(Fore.WHITE + "  [+] THREADS (1-5): " + Fore.YELLOW)
        threads = int(t_input) if t_input else 1
    except: threads = 1
    
    print(Fore.WHITE + " ─────────────────────────────────────────────")
    print_stats()
    
    try:
        with ThreadPoolExecutor(max_workers=threads) as executor:
            for num in numbers:
                executor.submit(worker, num)
                if threads > 1: time.sleep(3) 
    except KeyboardInterrupt:
        print(Fore.RED + "\n [!] Stopped.")
    finally:
        print(Fore.CYAN + "\n ─────────────────────────────────────────────")
        print(Fore.GREEN + " [✓] JOB COMPLETED.")

if __name__ == "__main__":
    main()
