from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main():
    driver = None

    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=options)

      
        driver.implicitly_wait(10)

        wait = WebDriverWait(driver, 15)

        print("WebDriver iniciado em modo Headless.")
        driver.get("https://the-internet.herokuapp.com/dropdown")
        aba0 = driver.current_window_handle

        handles_antes = set(driver.window_handles)

        driver.execute_script(
            "window.open('https://the-internet.herokuapp.com/"
            "dynamic_loading/2', '_blank');"
        )

        wait.until(
            lambda d: len(d.window_handles) > len(handles_antes)
        )

        aba1 = (
            set(driver.window_handles) - handles_antes
        ).pop()

        driver.switch_to.window(aba1)

        wait.until(
            EC.url_contains("/dynamic_loading/2")
        )

        print("Aba 1 aberta e validada:", driver.current_url)

        handles_antes = set(driver.window_handles)

        driver.execute_script(
            "window.open('https://pt.wikipedia.org/', '_blank');"
        )

        wait.until(
            lambda d: len(d.window_handles) > len(handles_antes)
        )

        aba2 = (
            set(driver.window_handles) - handles_antes
        ).pop()

        driver.switch_to.window(aba2)

        wait.until(
            EC.url_contains("pt.wikipedia.org")
        )

        print("Aba 2 aberta e validada:", driver.current_url)
        driver.switch_to.window(aba0)

        dropdown_element = wait.until(
            EC.presence_of_element_located(
                (By.ID, "dropdown")
            )
        )

        dropdown = Select(dropdown_element)
        dropdown.select_by_visible_text("Option 1")

        opcao_selecionada = dropdown.first_selected_option
        valor = opcao_selecionada.get_attribute("value")

        print("\n--- PARTE 3: Dropdown ---")
        print("Texto selecionado:", opcao_selecionada.text)
        print("Valor da opção:", valor)

  

        driver.switch_to.window(aba1)

        botao_start = wait.until(
            EC.element_to_be_clickable((By.ID, "start"))
        )
        botao_start.click()

        elemento_finish = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.ID, "finish"))
        )

        print("\n--- PARTE 4: Carregamento dinâmico ---")
        print("Texto retornado:", elemento_finish.text)
        driver.switch_to.window(aba2)
        campo_pesquisa = wait.until(
            EC.visibility_of_element_located(
                (By.ID, "searchInput")
            )
        )

        campo_pesquisa.send_keys("Automação")

       
        link = None

        try:
            link = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//div[@id='mw-panel']//a"
                        "[contains(normalize-space(.), "
                        "'Artigo destacado')]"
                    )
                )
            )
        except Exception:
            links = driver.find_elements(
                By.XPATH,
                "//div[@id='mw-panel']//a[@href]"
            )

            link = next(
                (
                    elemento for elemento in links
                    if elemento.text.strip()
                    and elemento.is_displayed()
                ),
                None
            )

        print("\n--- PARTE 5: Wikipédia ---")

        if link is not None:
            print("Texto do link:", link.text.strip())
            print("Destino (href):", link.get_attribute("href"))
        else:
            print("Nenhum link de navegação lateral foi localizado.")
        caminho = Path.cwd() / "evidencia_wiki.png"

        sucesso = driver.save_screenshot(str(caminho))

        if sucesso:
            print("Evidência salva em:", caminho.resolve())
        else:
            print("Não foi possível salvar a captura de tela.")

    except Exception as erro:
        print(f"Erro durante a execução: {type(erro).__name__}: {erro}")
        raise

    finally:
        if driver is not None:
            driver.quit()
            print("\nWebDriver encerrado.")


if __name__ == "__main__":
    main()
