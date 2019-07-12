import click
import dong
import dong.httpclient as httpclient
import dong.auth as auth

def _save(email, password):
    netrc = auth.load_netrc()
    netrc[dong.SERVER_NAME] = {
        'login': email,
        'password': password
    }
    netrc.save()


def _login(username, password):
    r = httpclient.post('api/v1/login/', json={'email': username, 'password': password})
    if r.status_code == 200:
        print("Login success!")

        password = r.json()['token']
        _save(
            email=username,
            password=password
        )
    else:
        print("Login failed")


@click.command(help='Login with your credentials.')
@click.option('-u', '--username', prompt=True)
@click.option('-p', '--password', prompt=True, hide_input=True)
def login(username, password):
    _login(username, password)
