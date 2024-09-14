from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, json, uuid

edge_options = Options()
# edge_options.add_argument("--headless")
edge_options.add_argument("--disable-gpu")
service = Service('C:\\Apps\\App\\edgedriver_win64\\msedgedriver.exe')
driver = webdriver.Edge(service=service, options=edge_options)

def parse(url):
    driver.get(url)
    time.sleep(4)

    for i in range(200):
        print(i)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

    media_grids = driver.find_elements(By.CLASS_NAME, "MediaGrid.MediaGrid--twoItems")

    images_dict = {}

    for grid in media_grids:
        left = grid.find_elements(By.CLASS_NAME, "MediaGrid__thumb.MediaGrid__thumb--left")
        right = grid.find_elements(By.CLASS_NAME, "MediaGrid__thumb.MediaGrid__thumb--right")
        for left_, right_ in zip(left, right):
            image_left = left_.find_elements(By.CLASS_NAME, "MediaGrid__imageElement")
            image_right = right_.find_elements(By.CLASS_NAME, "MediaGrid__imageElement")
            for image_l, image_r in zip(image_left, image_right):
                img1, img2 = image_l.get_attribute("src"), image_r.get_attribute("src")
                id = uuid.uuid4()
                if str(id) not in images_dict:
                    images_dict[str(id)] = {"left": None, "right": None}
                images_dict[str(id)]["left"] = img1
                images_dict[str(id)]["right"] = img2

    with open(f"images_{time.time()}.json", "w") as json_file:
        json.dump(images_dict, json_file, indent=4)

if __name__ == "__main__":
    url = "https://vk.com/9circles_of_hell"
    parse(url)
    driver.quit()


