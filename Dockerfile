FROM python_tgbot_env:1.0.0

WORKDIR /root/TgInnBot

COPY cred cred/
COPY logs logs/
COPY filters_table filters_table/
COPY msg_answer_builder msg_answer_builder/
COPY postgres postgres/
COPY google_sheet_custom_processor.py .
COPY inlineKeyBoardCollections.py .
COPY tgUser.py .
COPY UserManager.py .
COPY main.py .

EXPOSE 5000

CMD ["python3", "main.py"]

