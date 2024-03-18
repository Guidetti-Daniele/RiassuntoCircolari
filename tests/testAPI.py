import cheshire_cat_api as ccat
import json


def on_open():
    print('open')


def on_close(x, y):
    print('close')


def on_message(x):
    message = json.loads(x)

    print(x)


#    if message['type'] == 'chat':
#        print(message['content'])
#    else:
#        print('str')


def on_error(x):
    print(x)


# Connection settings with default values
config = ccat.Config(
    base_url="localhost",
    port=1865,
    user_id="user_2",
    auth_key="",
    secure_connection=False,
)

# Cat Client
cat_client = ccat.CatClient(
    config=config,
    on_open=on_open,
    on_close=on_close,
    on_message=on_message,
    on_error=on_error
)


def main():
    cat_client.connect_ws()

    while not cat_client.is_ws_connected:
        pass

    cat_client.send("ciao")

    while True:
        pass


if __name__ == '__main__':
    main()
