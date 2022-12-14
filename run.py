from main import MAL

def main():
    with MAL(collapse=True) as bot:
        bot.load_main_page()
        bot.load_and_accept_cookies()
        bot.accept_policy_button()
        bot.load_top_anime()
        bot.get_top_50_links()
        bot.scrap_all_data_for_top_50_animes()

if __name__ == "__main__":
    main()