import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
from dotenv import load_dotenv


start_time = time.time()

load_dotenv()

INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")

options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=options)

driver.get("https://www.instagram.com")
time.sleep(5)

try:
    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")

    username_input.send_keys(INSTAGRAM_USERNAME)
    password_input.send_keys(INSTAGRAM_PASSWORD)
    password_input.send_keys(Keys.RETURN)

    time.sleep(10)
    print("✅ Успешный вход в Instagram!")
except Exception as e:
    print("❌ Ошибка входа:", e)
    driver.quit()
    exit()

hashtag = "терминатор2"
url = f"https://www.instagram.com/explore/search/keyword/?q={hashtag}"
driver.get(url)
time.sleep(5)

# div_class_name = "xfcsdxf"
# div_element = driver.find_element(By.CLASS_NAME, div_class_name)  # Находим div с нужным классом

try:
    div_element = driver.find_element(By.XPATH, "//main[@role='main']").find_elements(By.XPATH, "./div")[0].find_elements(By.XPATH, "./div")[1]
except Exception as e:
    print(f"⚠️ Ошибка: {e}")





actions = ActionChains(driver)

data_list = []

previous_links = set()



MAX_CHECKS = 10  # 0 = бесконечно, любое другое число = ограничение
check_count = 0

while MAX_CHECKS == 0 or check_count < MAX_CHECKS:
    links = div_element.find_elements(By.TAG_NAME, "a")
    new_links_found = False

    for link in links:
        link_href = link.get_attribute("href")

        if not link_href or link_href in previous_links:
            continue

        previous_links.add(link_href)
        driver.execute_script("arguments[0].scrollIntoView({block: 'start'});", link)
        time.sleep(0.5)

        actions.move_to_element(link).perform()
        time.sleep(0.5)

        # 🔹 Кликаем на ссылку (открывает попап)
        link.click()
        time.sleep(1)  # Ожидаем загрузки попапа

        try:
            # 🔹 Ищем элемент "Просмотры:"
            view_text_elements = driver.find_elements(By.XPATH, "//span[contains(text(), 'Просмотры:')]")
            like_text_elements = driver.find_elements(By.XPATH, "//span[contains(text(), 'Нравится')]")

            view_count = None
            like_count = None

            if view_text_elements:
                for view_text in view_text_elements:
                    try:
                        view_count_span = view_text.find_element(By.TAG_NAME, "span")
                        view_count = view_count_span.text
                        break  # Берем первый найденный
                    except Exception as e:
                        print(f"⚠️ Ошибка при извлечении числа просмотров для {link_href}: {e}")

            if not view_count and like_text_elements:
                for like_text in like_text_elements:
                    try:
                        like_count_span = like_text.find_element(By.TAG_NAME, "span")
                        like_count = like_count_span.text
                        break  # Берем первый найденный
                    except Exception as e:
                        print(f"⚠️ Ошибка при извлечении числа лайков для {link_href}: {e}")

            # Если нет просмотров и лайков, ставим "0"
            data_list.append({
                "URL": link_href,
                "views": view_count if view_count else "Нет данных",
                "likes": like_count if like_count else "Нет данных",
            })

            print(
                f"🔗 {link_href} | 👀 Просмотры: {view_count if view_count else 'нет'} | ❤️ Лайки: {like_count if like_count else 'нет'}")

        except Exception as e:
            print(f"⚠️ Ошибка при поиске данных: {e}")

        try:
            # ⏳ Ждем появления SVG-кнопки закрытия (до 5 секунд)
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//*[name()='svg' and @aria-label='Закрыть']"))
            )

            # 🔍 Ищем SVG-кнопку закрытия
            close_svg = driver.find_element(By.XPATH, "//*[name()='svg' and @aria-label='Закрыть']")
            close_button = close_svg.find_element(By.XPATH, "./ancestor::div[@role='button']")

            # 🖱 Наводим мышку на кнопку перед кликом (если она заблокирована)
            actions.move_to_element(close_button).perform()
            time.sleep(0.5)

            # 🖱 Кликаем по кнопке
            close_button.click()

        except Exception as e:
            print(f"⚠️ Ошибка при закрытии попапа: {e}")

        new_links_found = True
        check_count += 1  # Увеличиваем счетчик, если не бесконечный режим

        if MAX_CHECKS > 0 and check_count >= MAX_CHECKS:
            print("✅ Достигнут лимит проверок, завершаем.")
            break

        time.sleep(1)

    if not new_links_found:
        print("⚠️ Новых ссылок нет, скроллим вниз...")
        driver.execute_script("window.scrollBy(0, 800);")
        time.sleep(3)

        new_links = div_element.find_elements(By.TAG_NAME, "a")
        if all(link.get_attribute("href") in previous_links for link in new_links):
            print("❌ Новых ссылок больше нет, завершаем.")
            break



print("\n✅ Собранные данные:")
for item in data_list:
    print(f"🔗 {item['URL']} | 👀 Просмотры: {item['views']} | ❤️ Лайки: {item['likes']}")

if data_list:
    df = pd.DataFrame(data_list)
    excel_filename = f"{hashtag}.xlsx"
    df.to_excel(excel_filename, index=False)
    print(f"📂 Данные сохранены в файл: {excel_filename}")
else:
    print("⚠️ Нет данных для сохранения.")

driver.quit()

end_time = time.time()

elapsed_time = end_time - start_time

hours = int(elapsed_time // 3600)
minutes = int((elapsed_time % 3600) // 60)
seconds = int(elapsed_time % 60)

print(f"⏰ Время выполнения: {hours}ч {minutes}м {seconds}с")