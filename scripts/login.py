# from playwright.sync_api import sync_playwright
# from playwright_stealth import Stealth
# from twocaptcha import TwoCaptcha
# import time
# import sys
# import getpass
# import random

# # 2Captcha API key (replace with your key from https://2captcha.com/)
# API_KEY = "280545057ef822e3834bf6f565433250"
# # Provided site key and URL
# SITE_KEY = "6LfXPFQlAAAAALoE7MuCiGzNoK4OHYlZRMtn8HCA"
# URL = "https://www.bhaskar.com/account/login?redirectURI=https%3A%2F%2Fwww.bhaskar.com%2Fepaper%2Fdetail-page%2Fraipur%2F116%2F2025-11-12"

# def solve_recaptcha_with_2captcha(page):
#     try:
#         print("Using 2Captcha to solve reCAPTCHA...")
#         solver = TwoCaptcha(API_KEY)
#         captcha_response = solver.recaptcha(
#             sitekey=SITE_KEY,
#             url=URL
#         )
#         recaptcha_token = captcha_response['code']
#         page.evaluate(f"""
#             () => {{
#                 const input = document.createElement('input');
#                 input.setAttribute('id', 'g-recaptcha-response');
#                 input.setAttribute('name', 'g-recaptcha-response');
#                 input.setAttribute('type', 'hidden');
#                 input.value = '{recaptcha_token}';
#                 document.body.appendChild(input);
#                 const event = new Event('change');
#                 input.dispatchEvent(event);
#             }}
#         """)
#         time.sleep(2)
#         print("2Captcha token injected. reCAPTCHA should be solved.")
#         return True
#     except Exception as e:
#         print(f"2Captcha solving failed: {str(e)}. Manual solve needed.")
#         return False

# def main():
#     with sync_playwright() as p:
#         # Launch Chrome browser (headed to reduce detection)
#         browser = p.chromium.launch(headless=False)
#         context = browser.new_context(
#             viewport={"width": 1280 + random.randint(-50, 50), "height": 720 + random.randint(-50, 50)},
#             user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
#             extra_http_headers={"Accept-Language": "en-US,en;q=0.9"},
#             locale="en-US",
#             timezone_id="Asia/Kolkata"  # Set to IST for India
#         )
#         # Apply Playwright Stealth to the context
#         Stealth().apply_stealth_sync(context)
#         # Add cookies to mimic real user
#         context.add_cookies([
#             {"name": "CONSENT", "value": "YES+cb.20251112-07-p0.en+FX", "domain": ".google.com", "path": "/"},
#             {"name": "_ga", "value": "GA1.2.123456789.1698765432", "domain": ".bhaskar.com", "path": "/"},
#             {"name": "_gid", "value": "GA1.2.987654321.1698765432", "domain": ".bhaskar.com", "path": "/"},
#             {"name": "_gat", "value": "1", "domain": ".bhaskar.com", "path": "/"}
#         ])
#         # Grant permissions to reduce bot-like behavior
#         context.grant_permissions(["geolocation", "notifications"])
#         page = context.new_page()

#         try:
#             print("Navigating to login page...")
#             page.goto(URL, wait_until="networkidle", timeout=30000)

#             # Wait for login form and phone input
#             print("Waiting for login form and phone input...")
#             phone_input = page.wait_for_selector(
#                 'input[placeholder*="मोबाइल नंबर"], input[placeholder*="mobile"], input[type="tel"], input[name="mobile"], #mobileNumber',
#                 timeout=20000,
#                 state="visible"
#             )
#             if not phone_input.is_visible():
#                 raise Exception("Phone input not visible.")

#             # Enter phone number with human-like typing
#             phone_number = "6299273276"
#             for digit in phone_number:
#                 phone_input.type(digit, delay=random.uniform(0.1, 0.3))
#                 time.sleep(random.uniform(0.05, 0.15))
#             print(f"Phone number {phone_number} entered.")

#             # Automate reCAPTCHA
#             print("Automating reCAPTCHA...")
#             max_attempts = 3
#             for attempt in range(1, max_attempts + 1):
#                 try:
#                     # Wait for reCAPTCHA iframe or challenge
#                     page.wait_for_selector(
#                         'iframe[src*="recaptcha/api2/anchor"]',
#                         timeout=20000
#                     )
#                     recaptcha_frame = page.frame_locator('iframe[src*="recaptcha/api2/anchor"]')
#                     recaptcha_checkbox = recaptcha_frame.locator(
#                         '#recaptcha-anchor, .recaptcha-checkbox-checkmark, .recaptcha-checkbox-border, [role="checkbox"]'
#                     ).first
#                     if recaptcha_checkbox.is_visible():
#                         print("reCAPTCHA checkbox found. Attempting to click...")
#                         bounding_box = recaptcha_checkbox.bounding_box()
#                         if bounding_box:
#                             x = bounding_box["x"] + bounding_box["width"] / 2
#                             y = bounding_box["y"] + bounding_box["height"] / 2
#                             page.mouse.move(x + random.uniform(-20, 20), y + random.uniform(-20, 20), steps=10)
#                             time.sleep(random.uniform(0.5, 1.0))
#                             page.mouse.click(x + random.uniform(-5, 5), y + random.uniform(-5, 5))
#                         else:
#                             recaptcha_checkbox.click()
#                         print(f"reCAPTCHA checkbox clicked (attempt {attempt}).")
#                         break
#                     else:
#                         raise Exception("reCAPTCHA checkbox not visible.")
#                 except Exception as e:
#                     print(f"Attempt {attempt} to handle reCAPTCHA failed: {str(e)}")
#                     if attempt == max_attempts:
#                         raise Exception("Failed to handle reCAPTCHA after retries.")
#                     time.sleep(2)

#             # Wait for reCAPTCHA to process and solve with 2Captcha
#             time.sleep(random.uniform(3, 5))
#             if page.locator('.rc-imageselect, iframe[src*="recaptcha"][title*="challenge"]').count() > 0:
#                 print("reCAPTCHA challenge detected. Using 2Captcha to solve...")
#                 if solve_recaptcha_with_2captcha(page):
#                     print("reCAPTCHA solved via 2Captcha.")
#                 else:
#                     print("2Captcha failed. Please solve the reCAPTCHA manually in the browser.")
#                     print("Instructions: Complete the challenge (e.g., select images), click 'Verify', then press Enter.")
#                     input("Press Enter to continue after manual solve: ")
#             else:
#                 print("No reCAPTCHA challenge detected; proceeding to submit.")

#             # Submit login form
#             print("Submitting login form...")
#             login_button = page.wait_for_selector(
#                 'button:has-text("लॉगिन"), button:has-text("Login"), .login-btn, #login, input[type="submit"]',
#                 timeout=10000,
#                 state="visible"
#             )
#             if login_button.is_visible():
#                 is_enabled = login_button.evaluate("el => !el.disabled")
#                 if not is_enabled:
#                     print("Warning: Login button is disabled. Waiting 3 seconds...")
#                     time.sleep(3)
#                     is_enabled = login_button.evaluate("el => !el.disabled")
#                     if not is_enabled:
#                         raise Exception("Login button remains disabled.")
#                 bounding_box = login_button.bounding_box()
#                 if bounding_box:
#                     x = bounding_box["x"] + bounding_box["width"] / 2
#                     y = bounding_box["y"] + bounding_box["height"] / 2
#                     page.mouse.move(x + random.uniform(-10, 10), y + random.uniform(-10, 10), steps=8)
#                     time.sleep(random.uniform(0.3, 0.6))
#                     page.mouse.click(x + random.uniform(-3, 3), y + random.uniform(-3, 3))
#                 else:
#                     login_button.click()
#                 print("Login form submitted. Waiting for OTP...")
#             else:
#                 raise Exception("Could not find login button.")

#             # Wait for OTP input field
#             print("Waiting for OTP input field...")
#             page.wait_for_selector(
#                 'input[type="text"][maxlength="6"], input[placeholder*="OTP"], input[placeholder*="ओटीपी"], #otpInput',
#                 timeout=30000
#             )

#             # Prompt for OTP
#             otp = getpass.getpass("Enter the 6-digit OTP received on your phone: ")
#             page.fill(
#                 'input[type="text"][maxlength="6"], input[placeholder*="OTP"], input[placeholder*="ओटीपी"], #otpInput',
#                 otp.strip()
#             )
#             print("OTP entered.")

#             # Submit OTP
#             page.click('button:has-text("Submit"), button:has-text("सबमिट"), .verify-otp-btn, input[type="submit"], #verifyOtp')
#             print("OTP submitted. Logging in...")

#             # Wait for redirect to ePaper
#             page.wait_for_load_state("networkidle")
#             page.wait_for_selector('iframe[src*="epaper"], .epaper-viewer, .content-unlocked', timeout=15000)
#             print("Login successful! Accessing ePaper...")

#             # Wait 5 seconds to view
#             time.sleep(5)

#         except Exception as e:
#             print(f"Error during automation: {str(e)}")
#             print("Page content snippet for debug:", page.content()[:2500])
#             print("Keeping browser open for 60 seconds to inspect the page...")
#             time.sleep(60)
#             sys.exit(1)
#         finally:
#             browser.close()
#             print("Browser closed.")

# if __name__ == "__main__":
#     main()
































# #####################################FIREFOX#######################################

# from playwright.sync_api import sync_playwright
# from playwright_stealth import Stealth
# import speech_recognition as sr
# from pydub import AudioSegment
# import io
# import time
# import sys
# import getpass
# import random
# import urllib.request

# def solve_audio_challenge(page):
#     try:
#         print("Switching to audio challenge...")
#         # Wait for challenge iframe (not anchor iframe)
#         challenge_frame = None
#         for attempt in range(1, 4):
#             try:
#                 page.wait_for_selector(
#                     'iframe[src*="recaptcha/api2/bframe"], iframe[title*="challenge"]',
#                     timeout=10000
#                 )
#                 challenge_frame = page.frame_locator('iframe[src*="recaptcha/api2/bframe"], iframe[title*="challenge"]')
#                 print(f"Challenge iframe found (attempt {attempt}).")
#                 break
#             except Exception as e:
#                 print(f"Attempt {attempt} to find challenge iframe failed: {str(e)}")
#                 if attempt == 3:
#                     raise Exception("Failed to find challenge iframe after retries.")
#                 time.sleep(2)

#         # Debug: Print iframe HTML
#         iframe_content = challenge_frame.locator('body').inner_html()
#         print("Challenge iframe HTML:", iframe_content[:1000])  # Truncated for brevity

#         # Click the audio icon in the challenge iframe
#         audio_link = challenge_frame.locator(
#             'button[aria-label*="audio"], .rc-audiochallenge-tab, #recaptcha-audio-button, a[href*="audio"], img[src*="audio"], .rc-button-audio'
#         ).first
#         if audio_link.is_visible():
#             audio_link.click()
#             time.sleep(3)
#             print("Audio challenge loaded.")
            
#             # Wait for audio download link
#             audio_download = challenge_frame.locator(
#                 'a[href*="audio.mp3"], .rc-audiochallenge-download-link, #audio-source'
#             ).first
#             if audio_download.is_visible():
#                 audio_url = audio_download.get_attribute('href')
#                 print(f"Downloading audio from {audio_url}")
#                 urllib.request.urlretrieve(audio_url, "recaptcha_audio.mp3")
                
#                 # Load and transcribe audio
#                 audio = AudioSegment.from_mp3("recaptcha_audio.mp3")
#                 audio.export("recaptcha_audio.wav", format="wav")
                
#                 r = sr.Recognizer()
#                 with sr.AudioFile("recaptcha_audio.wav") as source:
#                     audio_data = r.record(source)
#                     text = r.recognize_google(audio_data)
#                 print(f"Transcribed text: {text}")
                
#                 # Type transcribed text into audio input
#                 audio_input = challenge_frame.locator(
#                     'input[placeholder*="audio"], input[aria-label*="audio"], #audio-response'
#                 ).first
#                 if audio_input.is_visible():
#                     audio_input.fill(text)
#                     time.sleep(0.5)
#                     audio_input.press("Enter")
#                     time.sleep(3)
#                     print("Audio challenge submitted.")
#                     return True
#                 else:
#                     print("Audio input not found; manual solve needed.")
#             else:
#                 print("Audio download link not found; manual solve needed.")
#         else:
#             print("Audio link not visible; manual solve needed.")
#         return False
#     except Exception as e:
#         print(f"Audio solving failed: {str(e)}. Manual solve needed.")
#         return False

# def main():
#     with sync_playwright() as p:
#         # Launch Firefox browser (headed to reduce detection)
#         browser = p.firefox.launch(headless=False)
#         context = browser.new_context(
#             viewport={"width": 1280 + random.randint(-50, 50), "height": 720 + random.randint(-50, 50)},
#             user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
#             extra_http_headers={"Accept-Language": "en-US,en;q=0.9"},
#             locale="en-US",
#             timezone_id="Asia/Kolkata"  # Set to IST for India
#         )
#         # Apply Playwright Stealth to the context
#         Stealth().apply_stealth_sync(context)
#         # Add cookies to mimic real user
#         context.add_cookies([
#             {"name": "CONSENT", "value": "YES+cb.20251112-07-p0.en+FX", "domain": ".google.com", "path": "/"},
#             {"name": "_ga", "value": "GA1.2.123456789.1698765432", "domain": ".bhaskar.com", "path": "/"},
#             {"name": "_gid", "value": "GA1.2.987654321.1698765432", "domain": ".bhaskar.com", "path": "/"},
#             {"name": "_gat", "value": "1", "domain": ".bhaskar.com", "path": "/"}
#         ])
#         # Grant permissions to reduce bot-like behavior
#         context.grant_permissions(["geolocation", "notifications"])
#         page = context.new_page()

#         try:
#             print("Navigating to ePaper page...")
#             page.goto("https://www.bhaskar.com/epaper/detail-page/raipur/116/2025-11-12", wait_until="networkidle", timeout=30000)

#             # Wait for subscription modal and phone input
#             print("Waiting for subscription modal and phone input...")
#             phone_input = page.wait_for_selector(
#                 'input[placeholder*="मोबाइल नंबर"], input[placeholder*="mobile"], input[type="tel"], input[name="mobile"], #mobileNumber',
#                 timeout=20000,
#                 state="visible"
#             )
#             if not phone_input.is_visible():
#                 raise Exception("Phone input not visible.")

#             # Enter phone number with human-like typing
#             phone_number = "6299273276"
#             for digit in phone_number:
#                 phone_input.type(digit, delay=random.uniform(0.1, 0.3))
#                 time.sleep(random.uniform(0.05, 0.15))
#             print(f"Phone number {phone_number} entered.")

#             # Automate reCAPTCHA checkbox
#             print("Automating reCAPTCHA checkbox...")
#             # Wait for reCAPTCHA iframe
#             max_attempts = 3
#             recaptcha_frame = None
#             for attempt in range(1, max_attempts + 1):
#                 try:
#                     page.wait_for_selector(
#                         'iframe[src*="recaptcha/api2/anchor"]',
#                         timeout=20000
#                     )
#                     recaptcha_frame = page.frame_locator('iframe[src*="recaptcha/api2/anchor"]')
#                     print(f"reCAPTCHA iframe found (attempt {attempt}).")
#                     break
#                 except Exception as e:
#                     print(f"Attempt {attempt} to find reCAPTCHA iframe failed: {str(e)}")
#                     if attempt == max_attempts:
#                         raise Exception("Failed to find reCAPTCHA iframe after retries.")
#                     time.sleep(2)

#             # Target checkbox within iframe
#             recaptcha_checkbox = recaptcha_frame.locator(
#                 '#recaptcha-anchor, .recaptcha-checkbox-checkmark, .recaptcha-checkbox-border, [role="checkbox"]'
#             ).first
#             if recaptcha_checkbox.is_visible():
#                 print("reCAPTCHA checkbox found. Attempting to click...")
#                 # Simulate human-like behavior
#                 page.evaluate("window.scrollBy(0, 100)")  # Scroll to ensure visibility
#                 for attempt in range(1, max_attempts + 1):
#                     try:
#                         bounding_box = recaptcha_checkbox.bounding_box()
#                         if bounding_box:
#                             x = bounding_box["x"] + bounding_box["width"] / 2
#                             y = bounding_box["y"] + bounding_box["height"] / 2
#                             page.mouse.move(x + random.uniform(-20, 20), y + random.uniform(-20, 20), steps=10)
#                             time.sleep(random.uniform(0.5, 1.0))
#                             page.mouse.click(x + random.uniform(-5, 5), y + random.uniform(-5, 5))
#                         else:
#                             recaptcha_checkbox.click()
#                         print(f"reCAPTCHA checkbox clicked (attempt {attempt}).")
#                         break
#                     except Exception as e:
#                         print(f"Attempt {attempt} to click reCAPTCHA checkbox failed: {str(e)}")
#                         if attempt == max_attempts:
#                             raise Exception("Failed to click reCAPTCHA checkbox after retries.")
#                         time.sleep(1)

#                 # Inject JavaScript to bypass reCAPTCHA checks
#                 page.evaluate("""
#                     () => {
#                         const checkbox = document.querySelector('#recaptcha-anchor, .recaptcha-checkbox-checkmark');
#                         if (checkbox) {
#                             checkbox.setAttribute('aria-checked', 'true');
#                             checkbox.classList.add('recaptcha-checkbox-checked');
#                         }
#                         const response = document.getElementById('g-recaptcha-response');
#                         if (response) {
#                             response.value = 'simulated_token';
#                             response.dispatchEvent(new Event('change'));
#                         }
#                     }
#                 """)

#                 # Wait for reCAPTCHA to process
#                 time.sleep(random.uniform(3, 5))

#                 # Check for image challenge and solve with audio method
#                 if page.locator('.rc-imageselect, iframe[src*="recaptcha"][title*="challenge"]').count() > 0:
#                     print("Image reCAPTCHA challenge detected. Attempting automatic audio bypass...")
#                     if solve_audio_challenge(page):
#                         print("Audio challenge solved automatically.")
#                     else:
#                         print("Audio bypass failed. Please solve the image reCAPTCHA manually in the browser.")
#                         print("Instructions: Select the required images (e.g., traffic lights), click 'Verify', then press Enter in the terminal.")
#                         input("Press Enter to continue after manual solve: ")
#                 else:
#                     print("No reCAPTCHA challenge detected; proceeding to click 'जारी रखें'.")
#             else:
#                 print("reCAPTCHA checkbox not visible; proceeding to click 'जारी रखें'.")

#             # Automatically click "जारी रखें" (Continue) button
#             print("Automatically clicking 'जारी रखें' button...")
#             continue_button = page.wait_for_selector(
#                 'button:has-text("जारी रखें"), button:has-text("Continue"), .continue-btn, #continue, input[type="submit"], [type="submit"], button:not([disabled])',
#                 timeout=10000,
#                 state="visible"
#             )
#             if continue_button.is_visible():
#                 # Verify button is enabled
#                 is_enabled = continue_button.evaluate("el => !el.disabled")
#                 if not is_enabled:
#                     print("Warning: 'जारी रखें' button is disabled. Waiting 3 seconds...")
#                     time.sleep(3)
#                     is_enabled = continue_button.evaluate("el => !el.disabled")
#                     if not is_enabled:
#                         raise Exception("'जारी रखें' button remains disabled.")

#                 # Simulate human-like click
#                 bounding_box = continue_button.bounding_box()
#                 if bounding_box:
#                     x = bounding_box["x"] + bounding_box["width"] / 2
#                     y = bounding_box["y"] + bounding_box["height"] / 2
#                     page.mouse.move(x + random.uniform(-10, 10), y + random.uniform(-10, 10), steps=8)
#                     time.sleep(random.uniform(0.3, 0.6))
#                     page.mouse.click(x + random.uniform(-3, 3), y + random.uniform(-3, 3))
#                 else:
#                     continue_button.click()
#                 print("'जारी रखें' button clicked. Waiting for OTP...")
#             else:
#                 raise Exception("Could not find 'जारी रखें' button.")

#             # Wait for OTP input field
#             print("Waiting for OTP input field...")
#             page.wait_for_selector(
#                 'input[type="text"][maxlength="6"], input[placeholder*="OTP"], input[placeholder*="ओटीपी"], #otpInput',
#                 timeout=30000
#             )

#             # Prompt for OTP
#             otp = getpass.getpass("Enter the 6-digit OTP received on your phone: ")
#             page.fill(
#                 'input[type="text"][maxlength="6"], input[placeholder*="OTP"], input[placeholder*="ओटीपी"], #otpInput',
#                 otp.strip()
#             )
#             print("OTP entered.")

#             # Submit OTP
#             page.click('button:has-text("Submit"), button:has-text("सबमिट"), .verify-otp-btn, input[type="submit"], #verifyOtp')
#             print("OTP submitted. Logging in...")

#             # Wait for login success (ePaper unlocks)
#             page.wait_for_load_state("networkidle")
#             page.wait_for_selector('iframe[src*="epaper"], .epaper-viewer, .content-unlocked', timeout=15000)
#             print("Login successful! Accessing ePaper...")

#             # Wait 5 seconds to view
#             time.sleep(5)

#         except Exception as e:
#             print(f"Error during automation: {str(e)}")
#             print("Page content snippet for debug:", page.content()[:2500])
#             print("Keeping browser open for 60 seconds to inspect the page...")
#             time.sleep(60)
#             sys.exit(1)
#         finally:
#             browser.close()
#             print("Browser closed.")

# if __name__ == "__main__":
#     main()




























###############################CHROME#######################################
import os
import sys
import time
import random
import getpass
import urllib.request
from pydub import AudioSegment
import speech_recognition as sr
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

# --------------------- CONFIG ---------------------
PHONE_NUMBER = "6299273276"
EPAPER_DATE = "2025-11-13"  # Today
URL = f"https://www.bhaskar.com/epaper/detail-page/raipur/116/{EPAPER_DATE}"
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15"
]
# Replace with a valid proxy if available (e.g., "http://user:pass@proxy:port")
PROXY = None  # Set to None or a proxy string
# --------------------------------------------------

def solve_audio_challenge(page):
    print("Attempting automatic audio reCAPTCHA solving...")
    max_audio_attempts = 3  # Increased retries for audio
    for audio_attempt in range(max_audio_attempts):
        try:
            # Wait for challenge iframe with retries
            challenge_frame = None
            for attempt in range(1, 4):
                try:
                    page.wait_for_selector(
                        'iframe[src*="recaptcha/api2/bframe"], iframe[title*="challenge"]',
                        timeout=10000
                    )
                    challenge_frame = page.frame_locator('iframe[src*="recaptcha/api2/bframe"], iframe[title*="challenge"]').first
                    print(f"Challenge iframe found (attempt {attempt}).")
                    break
                except Exception as e:
                    print(f"Attempt {attempt} to find challenge iframe failed: {str(e)}")
                    if attempt == 3:
                        raise Exception("Failed to find challenge iframe after retries.")
                    time.sleep(random.uniform(1, 3))

            # Click the audio challenge button
            audio_btn = challenge_frame.locator(
                'button[aria-label*="audio"], .rc-button-audio, #recaptcha-audio-button, button.rc-button-default'
            ).first
            if audio_btn.is_visible():
                audio_btn.click()
                print("Audio challenge loaded.")
                time.sleep(random.uniform(3, 5))

                # Wait for audio download link with separate XPath and CSS selectors
                audio_download = None
                for attempt in range(1, 5):
                    try:
                        # Try XPath first
                        audio_download_xpath = challenge_frame.locator(
                            'xpath=//div[contains(@class, "rc-audiochallenge-tdownload")]//a'
                        ).first
                        if audio_download_xpath.is_visible():
                            audio_download = audio_download_xpath
                            break
                        # Try CSS as fallback
                        audio_download_css = challenge_frame.locator(
                            'a[href*="audio.mp3"], .rc-audiochallenge-download-link'
                        ).first
                        if audio_download_css.is_visible():
                            audio_download = audio_download_css
                            break
                        time.sleep(random.uniform(2, 4))
                    except Exception as e:
                        print(f"Attempt {attempt} to find audio download failed: {str(e)}")
                        if attempt == 4:
                            print("Audio download link not found, skipping to JavaScript bypass.")
                            return False

                audio_url = audio_download.get_attribute('href')
                if not audio_url:
                    raise Exception("Audio URL is None")
                print(f"Downloading audio from {audio_url}")
                urllib.request.urlretrieve(audio_url, "recaptcha_audio.mp3")

                # Convert and transcribe audio
                audio = AudioSegment.from_mp3("recaptcha_audio.mp3")
                audio.export("recaptcha_audio.wav", format="wav")
                r = sr.Recognizer()
                with sr.AudioFile("recaptcha_audio.wav") as source:
                    audio_data = r.record(source)
                text = r.recognize_google(audio_data)
                print(f"Transcribed text: {text}")

                # Enter the answer
                audio_input = challenge_frame.locator(
                    'input[aria-label*="audio"], #audio-response, input[placeholder*="Enter"]'
                ).first
                if audio_input.is_visible():
                    audio_input.fill(text)
                    time.sleep(random.uniform(0.5, 1.0))
                    audio_input.press("Enter")
                    print("Audio challenge submitted.")
                    # Wait briefly to allow server response
                    time.sleep(random.uniform(5, 10))  # Extended wait for server processing
                    return True  # Proceed after submission, skipping strict validation
                else:
                    print("Audio input not found.")
            else:
                print("Audio button not visible.")
            return False
        except Exception as e:
            print(f"Audio solving attempt {audio_attempt + 1} failed: {str(e)}")
            if audio_attempt < max_audio_attempts - 1:
                print("Retrying audio challenge...")
                time.sleep(random.uniform(2, 4))
                continue
            print("All audio attempts failed. Attempting enhanced JavaScript bypass...")
            # Enhanced JavaScript fallback with loop
            max_attempts = 3
            for attempt in range(max_attempts):
                page.evaluate("""
                    () => {
                        const response = document.getElementById('g-recaptcha-response');
                        if (response) {
                            response.value = 'simulated_token_' + Math.random().toString(36).substr(2, 9);
                            response.dispatchEvent(new Event('change'));
                            response.dispatchEvent(new Event('input'));
                        }
                        const checkbox = document.querySelector('.recaptcha-checkbox');
                        if (checkbox) {
                            checkbox.setAttribute('aria-checked', 'true');
                            checkbox.classList.add('recaptcha-checkbox-checked');
                        }
                        const verify = document.querySelector('.recaptcha-verify-button');
                        if (verify) verify.click();
                        const audioResponse = document.querySelector('#audio-response');
                        if (audioResponse) audioResponse.value = 'PASSED';
                    }
                """)
                time.sleep(random.uniform(2, 4))
                try:
                    page.wait_for_function(
                        "document.querySelector('.recaptcha-checkbox-checked') && !document.querySelector('button:disabled')",
                        timeout=15000
                    )
                    print(f"reCAPTCHA resolved after JavaScript attempt {attempt + 1}")
                    return True
                except Exception:
                    print(f"JavaScript attempt {attempt + 1} failed, retrying...")
                    if attempt == max_attempts - 1:
                        print("JavaScript bypass failed after maximum attempts.")
                        return False
            return False

def main():
    max_retries = 3
    for retry in range(max_retries):
        with sync_playwright() as p:
            # Launch Chrome browser with random user agent and proxy if available
            browser = p.chromium.launch(headless=False, proxy=PROXY)
            context = browser.new_context(
                viewport={"width": 1280 + random.randint(-50, 50), "height": 720 + random.randint(-50, 50)},
                user_agent=random.choice(USER_AGENTS),
                extra_http_headers={"Accept-Language": "en-IN,en;q=0.9"},
                locale="en-IN",
                timezone_id="Asia/Kolkata"  # Set to IST for India
            )
            # Apply Playwright Stealth to the context
            Stealth().apply_stealth_sync(context)
            # Add cookies to mimic real user
            context.add_cookies([
                {"name": "CONSENT", "value": "YES+cb.20251113-07-p0.en+FX", "domain": ".google.com", "path": "/"},
                {"name": "_ga", "value": "GA1.2.123456789.1698765432", "domain": ".bhaskar.com", "path": "/"},
                {"name": "_gid", "value": "GA1.2.987654321.1698765432", "domain": ".bhaskar.com", "path": "/"},
                {"name": "_gat", "value": "1", "domain": ".bhaskar.com", "path": "/"}
            ])
            # Grant permissions to reduce bot-like behavior
            context.grant_permissions(["geolocation", "notifications"])
            page = context.new_page()
            try:
                print(f"Navigating to ePaper page... (Attempt {retry + 1}/{max_retries})")
                page.goto(URL, wait_until="networkidle", timeout=30000)
                # Check for automated query detection early
                if page.locator('text="Your computer or network may be sending automated queries"').count() > 0:
                    print("Automated query detection triggered before interaction. Retrying...")
                    time.sleep(random.uniform(5, 10))
                    continue

                # Wait for subscription modal and phone input
                print("Waiting for subscription modal and phone input...")
                phone_input = page.wait_for_selector(
                    'input[placeholder*="मोबाइल नंबर"], input[placeholder*="mobile"], input[type="tel"], input[name="mobile"], #mobileNumber',
                    timeout=20000,
                    state="visible"
                )
                if not phone_input.is_visible():
                    raise Exception("Phone input not visible.")
                # Enter phone number with human-like typing
                for digit in PHONE_NUMBER:
                    phone_input.type(digit, delay=random.uniform(0.1, 0.3))
                    time.sleep(random.uniform(0.05, 0.15))
                print(f"Phone number {PHONE_NUMBER} entered.")

                # Automate reCAPTCHA checkbox
                print("Automating reCAPTCHA checkbox...")
                # Wait for reCAPTCHA iframe
                max_attempts = 3
                recaptcha_frame = None
                for attempt in range(1, max_attempts + 1):
                    try:
                        page.wait_for_selector(
                            'iframe[src*="recaptcha/api2/anchor"]',
                            timeout=20000
                        )
                        recaptcha_frame = page.frame_locator('iframe[src*="recaptcha/api2/anchor"]').first
                        print(f"reCAPTCHA iframe found (attempt {attempt}).")
                        break
                    except Exception as e:
                        print(f"Attempt {attempt} to find reCAPTCHA iframe failed: {str(e)}")
                        if attempt == max_attempts:
                            raise Exception("Failed to find reCAPTCHA iframe after retries.")
                        time.sleep(random.uniform(1, 3))
                # Target checkbox within iframe
                recaptcha_checkbox = recaptcha_frame.locator(
                    '#recaptcha-anchor, .recaptcha-checkbox-checkmark, .recaptcha-checkbox-border, [role="checkbox"]'
                ).first
                if recaptcha_checkbox.is_visible():
                    print("reCAPTCHA checkbox found. Attempting to click...")
                    # Simulate human-like behavior
                    page.evaluate("window.scrollBy(0, 100)")
                    for attempt in range(1, max_attempts + 1):
                        try:
                            bounding_box = recaptcha_checkbox.bounding_box()
                            if bounding_box:
                                x = bounding_box["x"] + bounding_box["width"] / 2
                                y = bounding_box["y"] + bounding_box["height"] / 2
                                page.mouse.move(x + random.uniform(-20, 20), y + random.uniform(-20, 20), steps=10)
                                time.sleep(random.uniform(0.5, 1.0))
                                page.mouse.click(x + random.uniform(-5, 5), y + random.uniform(-5, 5))
                            else:
                                recaptcha_checkbox.click()
                            print(f"reCAPTCHA checkbox clicked (attempt {attempt}).")
                            break
                        except Exception as e:
                            print(f"Attempt {attempt} to click reCAPTCHA checkbox failed: {str(e)}")
                            if attempt == max_attempts:
                                raise Exception("Failed to click reCAPTCHA checkbox after retries.")
                            time.sleep(random.uniform(1, 2))
                    # Wait for challenge to load
                    time.sleep(random.uniform(3, 5))
                    # Check for challenge and solve
                    if page.locator('.rc-imageselect, iframe[src*="recaptcha"][title*="challenge"]').count() > 0:
                        print("Image reCAPTCHA challenge detected. Attempting automatic bypass...")
                        solve_audio_challenge(page)  # Call without condition
                    else:
                        print("No reCAPTCHA challenge detected; proceeding to click 'जारी रखें'.")

                # Enhanced approach to click "जारी रखें" button
                print("Attempting to click 'जारी रखें' button with enhanced approach...")
                max_button_attempts = 3
                continue_button = page.wait_for_selector(
                    'button:has-text("जारी रखें"), button:has-text("Continue"), .continue-btn, #continue, input[type="submit"], [type="submit"]',
                    timeout=20000,
                    state="visible"
                )
                if continue_button.is_visible():
                    for attempt in range(max_button_attempts):
                        try:
                            # Check if button is interactable
                            is_enabled = continue_button.evaluate("el => !el.disabled && el.offsetParent !== null")
                            if is_enabled:
                                print(f"Button detected as enabled on attempt {attempt + 1}")
                                # Try multiple click methods
                                try:
                                    bounding_box = continue_button.bounding_box()
                                    if bounding_box:
                                        x = bounding_box["x"] + bounding_box["width"] / 2
                                        y = bounding_box["y"] + bounding_box["height"] / 2
                                        page.mouse.move(x + random.uniform(-10, 10), y + random.uniform(-10, 10), steps=8)
                                        time.sleep(random.uniform(0.3, 0.6))
                                        page.mouse.click(x + random.uniform(-3, 3), y + random.uniform(-3, 3))
                                    else:
                                        continue_button.click()
                                    print(f"'जारी रखें' button clicked on attempt {attempt + 1}")
                                    # Wait for navigation or OTP
                                    page.wait_for_load_state("networkidle", timeout=15000)
                                    if page.locator('input[type="text"][maxlength="6"], input[placeholder*="OTP"]').count() > 0:
                                        print("Next page detected, proceeding to OTP...")
                                        break
                                    else:
                                        print("No OTP input detected, retrying click...")
                                        time.sleep(random.uniform(2, 4))
                                        continue
                                except Exception as e:
                                    print(f"Click method 1 failed on attempt {attempt + 1}: {str(e)}")
                            else:
                                print(f"Button not enabled on attempt {attempt + 1}, waiting...")
                                time.sleep(random.uniform(2, 4))
                                page.wait_for_function("!document.querySelector('button:disabled')", timeout=20000)
                            # Fallback: Trigger form submission if button is part of a form
                            page.evaluate("""
                                () => {
                                    const button = document.querySelector('button:has-text("जारी रखें"), button:has-text("Continue")');
                                    if (button && button.form) button.form.submit();
                                }
                            """)
                            print(f"Form submission triggered on attempt {attempt + 1}")
                            page.wait_for_load_state("networkidle", timeout=15000)
                            if page.locator('input[type="text"][maxlength="6"], input[placeholder*="OTP"]').count() > 0:
                                print("Next page detected after form submission, proceeding to OTP...")
                                break
                            else:
                                print("No OTP input after form submission, retrying...")
                                time.sleep(random.uniform(2, 4))
                                continue
                        except Exception as e:
                            print(f"Button click attempt {attempt + 1} failed: {str(e)}")
                            if attempt == max_button_attempts - 1:
                                raise Exception("'जारी रखें' button remains unclickable after maximum attempts.")
                            time.sleep(random.uniform(2, 4))
                else:
                    raise Exception("Could not find 'जारी रखें' button.")

                # Wait for OTP input field
                print("Waiting for OTP input field...")
                page.wait_for_selector(
                    'input[type="text"][maxlength="6"], input[placeholder*="OTP"], input[placeholder*="ओटीपी"], #otpInput',
                    timeout=30000
                )
                # Prompt for OTP
                otp = getpass.getpass("Enter the 6-digit OTP received on your phone: ")
                page.fill(
                    'input[type="text"][maxlength="6"], input[placeholder*="OTP"], input[placeholder*="ओटीपी"], #otpInput',
                    otp.strip()
                )
                print("OTP entered.")

                # Submit OTP
                page.click('button:has-text("Submit"), button:has-text("सबमिट"), .verify-otp-btn, input[type="submit"], #verifyOtp')
                print("OTP submitted. Logging in...")

                # Wait for login success (ePaper unlocks)
                page.wait_for_load_state("networkidle")
                page.wait_for_selector('iframe[src*="epaper"], .epaper-viewer, .content-unlocked', timeout=15000)
                print("Login successful! Accessing ePaper...")
                time.sleep(5)
                break  # Exit retry loop on success

            except Exception as e:
                print(f"Error during automation: {str(e)}")
                print("Page content snippet for debug:", page.content()[:2500])
                print("Keeping browser open for 60 seconds to inspect the page...")
                time.sleep(60)
                if retry < max_retries - 1 and ("automated queries" in str(e).lower() or page.locator('text="Your computer or network may be sending automated queries"').count() > 0):
                    print("Retrying due to automated query detection or other error...")
                    time.sleep(random.uniform(5, 10))
                    continue
                sys.exit(1)
            finally:
                browser.close()
                print("Browser closed.")

if __name__ == "__main__":
    main()