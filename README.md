Virtualis client
================

> A console client for [Virtualis] API.

[Virtualis]: http://www.service-virtualis.com/

Overview
--------

Virtualis is a service developed by the *Crédit Mutuel*, to allow bank
clients to create virtual credit cards with amount limit and custom
expiration date. The following financial institutions give a Virtualis
access to their clients (list from [Virtualis website][list]):

[list]: http://www.service-virtualis.com/virtualis/paiement_nomade.htm

* Credit Mutuel de Bretagne (CMB)
* Credit Mutuel Massif Central (CMMC)
* Credit Mutuel Sud Ouest (CMSO)
* Banque Privée Européenne (BPE)
* Arkéa Banque Privée (ABP)
* ARKEA Banque Entreprises et Institutionnels
* Fortunéo
* BEMIX

While I like the features provided by this service, I'm not satisfied
with the few ways they provide to access this API; a Microsoft Windows
binary and an Adobe Flash application. I'm not using both of these
softwares, *mainly because their licenses are not acceptable to me*.

That's why I reverse engineered their Flash client, to understand how
works their protocol, [document it](api.md), build a [Python
library](virtualis) and a [command-line client](virtualis-client).

This project's purpose is to publish a free and open-source way to
access the Virtualis API, without any dependency on softwares with an
unacceptable license.

Dependencies
------------

* `python3`
  * `docopt` <https://pypi.python.org/pypi/docopt>

Library
-------

The library is composed of a [client](virtualis/client.py) and a set of
[methods](virtualis/methods) wrapping the available [API requests](api.md).

### Create the client

To get started, you need to instanciate a client:

```python
import getpass
import virtualis

user = '0000000000'
pass = getpass.getpass() # Prompt the user for password

client = virtualis.Client(user, pass, capath='/etc/ssl/certs')
```

The `capath` parameter is required to let the SSL client know where the
trusted SSL CA certificates are stored on your computer. The above
location is really common for GNU/Linux distributions.

You can also pass a single file with `cafile` option, for example on
FreeBSD, set it to `/usr/local/share/certs/ca-root-nss.crt` to use the
system CA certificates.

See [this message](http://bugs.python.org/issue13655#msg192601) for more
common locations. Otherwise, you can download the [Mozilla CA bundle]
from cURL website.

[Mozilla CA bundle]: http://curl.haxx.se/docs/caextract.html

### Get the cards

The first thing you wanna make is retrieve the list of *physical* cards
associated to this account, because you need this to work with virtual
cards. This request takes no parameters.

```python
request = virtualis.CardsRequest()
response = client.send(request)
cards = response.cards
```

Here, `cards` is a list of `Card` objects with properties defined
[here](virtualis/methods/cards.py).

### Get the virtual cards

Now you may want to list the virtual cards for one of the previous
*physical* cards. Here, we take the first card of the previous list.

Since there may be a lot of virtual cards, the API implements a
pagination system. I created a friendly `paginate` method for this.

```python
request = virtualis.VirtualCardsRequest(cards[0])
request.paginate(1, 10) # Get the first page with 10 items per page
response = client.send(request)

print(response.count) # The total number of virtual cards
print(response.cards)

request.paginate(2, 10) # Get the next set
response = client.send(request)

print(response.cards)
```

If you want to list all the virtual cards, you can keep paginating until
you have `response.count` (or in other words, make `ceil(response.count /
limit)` requests (`limit` being the number of items per page). See the
`ipagination` function from [`virtualis-client`](virtualis-client) for
an example.

### Other methods

You can watch the other [methods](virtualis/methods) to see what's
available, and look the request/response classes to see what arguments
you need to pass, and what informations you will get back. Also check
the [API](api.md) documentation for more verbose informations about
request and response parameters.

And don't forget to watch [`virtualis-client`](virtualis-client) which
is a great example of API usage.

Client
------

The console client is a frontend to the library, allowing you to manage
your Virtualis account from the command-line.

For now, the frontend is in the form of a shell-like interface where you
have commands to manipulate your account. This is a captive interface,
and won't allow you to easily pipe a command's output into other Unix
tools. That's a UX disaster I'm willing to change, by developing a new
client inspired by the nmh mail client. See [`TODO.md`](TODO.md) for
more on this.

### Launching the client

Run `virtualis-client --help` to see the usage string and options.

If your user ID is `0004201337`, run the following:

```sh
virtualis-client 0004201337
```

You will be prompted for your password, and if everything's okay, you'll
jump into a shell-like interface.

If your credentials are wrong, an exception is thrown and you have to
restart the program.

You may encounter a SSL validation error. If your CA certificates are
not in the default path (`/etc/ssl/certs`), be sure to pass one of the
`--cafile` or `--capath` options. This is already documented [for the
library](#create-the-client).

Run `help` to see the available commands, and `help <command>` to see a
specific command's help.

### List the cards

`TODO`

### List the virtual cards

`TODO`

### Create a card

`TODO`

### Delete a card

`TODO`

### List a card's transactions

`TODO`
