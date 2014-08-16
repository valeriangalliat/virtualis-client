Virtualis API
=============

* [Format](#format)
* [Types](#types)
* [Arrays](#arrays)
* [Pagination](#pagination)
* [Common request parameters](#common-request-parameters)
* [Common response parameters](#common-response-parameters)
* [Authentication](#authentication)
* [Session](#session)
* [Errors](#errors)
* [Methods](#methods)
  * [Cards](#cards)
  * [Virtual cards](#virtual-cards)
  * [Create card](#create-card)
  * [Delete card](#delete-card)
  * [Profiles list](#profiles-list)
  * [Shipping profile](#shipping-profile)
  * [Buyings](#buyings)

Format
------

All the API calls are made on <https://service-virtualis.com/cvd/WebServlet>
using the `POST` HTTP method.

All requests are made with `application/x-www-form-urlencoded` content type.

The request data must be encoded in ISO 8859-1, and the returned data
is in the same encoding.

Do not trust the `Content-Type` response header at all. They always set it to
`text/html; charset=UTF-8` even if they're actually sending
`application/x-www-form-urlencoded; charset=ISO-8859-1`.

All urlencoded responses can contain a trailing `&`, or multiple `&` (empty
parameters). In a strict parsing, you should remove them first.

The responses won't contain any array parameter (like `foo[]=bar`), and
you can safely assume each parameter is unique.

Types
-----

Some custom types can be found in multiple parameters:

<table>
  <thead>
    <tr>
      <th>Name</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>string boolean</td>
      <td>whether the string is <code>true</code> or <code>false</code></td>
    </tr>
    <tr>
      <td>yes/no</td>
      <td><code>Y</code> or <code>N</code></td>
    </tr>
    <tr>
      <td>date</td>
      <td>
        <code>day/month/year</code>, 2 digits for day and month,
        4 for year
      </td>
    </tr>
    <tr>
      <td>short date</td>
      <td>2 digits for month and year</td>
    </tr>
    <tr>
      <td>money</td>
      <td>
        the first character is an URL encoded money symbol (like
        <code>%80</code> for <code>€</code>), followed by a float number
        with <code>.</code> as decimal separator
      </td>
    </tr>
  </tbody>
</table>

Arrays
------

Some requests returns array-like structures. This is done with a `Total`
response parameter, and multiple parameters ending with an integer
representing the offset.

### Examples

    Total: 2
    Foo1: value
    Bar1: value
    Foo2: value
    Bar2: value

I'll write these parameters ending with the `[x]` sequence, meant to be
replaced with a number, from 0 to `Total`:

    Foo[x]
    Bar[x]

Pagination
----------

Some requests support pagination. This is done with additional parameters
in the request and the response:

### Request

| Name    | Type    | Description                              |
| ------- | ------- | ---------------------------------------- |
| `Start` | integer | start offset (0 for the first item)      |
| `Next`  | integer | number of records to fetch after `Start` |

In the official application, there is 20 items per page.

### Response

| Name          | Type    | Description                       |
| ------------- | ------- | --------------------------------- |
| `RecordCount` | integer | total number of records           |
| `Start`       | integer | same as `Start` request parameter |
| `End`         | integer | last record of the set            |

Note the pagination seems to be tied to the session. The request will fail
if you give a non-zero `Start` for the first request. Once the first
request is done, you can paginate as you want.

### Examples

Fetch the first 4 items:

    Start: 0
    Next: 4
    ---
    RecordCount: 16
    Start: 0
    End: 3

Fetch the second page of the previous request:

    Start: 4
    Next: 4
    ---
    RecordCount: 16
    Start: 4
    End: 7

Fetch the last record:

    Start: 15
    Next: 1
    ---
    RecordCount: 16
    Start: 15
    End: 15

Common request parameters
-------------------------

<table>
  <thead>
    <tr>
      <th>Name</th>
      <th>Type</th>
      <th>Description</th>
      <th>Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>Version</code></td>
      <td>string</td>
      <td>probably the client or server version</td>
      <td><code>3.0</code></td>
    </tr>
    <tr>
      <td><code>IssuerId</code></td>
      <td>integer</td>
      <td></td>
      <td><code>1</code></td>
    </tr>
    <tr>
      <td><code>Locale</code></td>
      <td>string</td>
      <td>
        client locale, two letter country code (like <code>fr</code>),
        required for some requests like <code>GetCPN</code>
      </td>
      <td></td>
    </tr>
    <tr>
      <td><code>Trigger</code></td>
      <td>string</td>
      <td></td>
      <td><code>trigger</code></td>
    </tr>
    <tr>
      <td><code>IE</code></td>
      <td>string boolean</td>
      <td>
        probably whether the client is Microsoft Internet Explorer, you
        can set it to <code>true</code> if you want to troll their browser
        statistics
      </td>
      <td></td>
    </tr>
    <tr>
      <td><code>startTime</code></td>
      <td>integer</td>
      <td>
        maybe the time since last request... <code>0</code> seems to be
        valid
      </td>
      <td></td>
    </tr>
  </tbody>
</table>

Common response parameters
--------------------------

| Name     | Type           | Description                           |
| ---------| ---------------| ------------------------------------- |
| `Action` | string         | probably the client action to trigger |
| `Eof`    | string boolean |                                       |


Authentication
--------------

For the first request (when you have no cookie, nor `SessionId`), you
have to append these parameters to the request body:

| Name         | Description           |
| ------------ | --------------------- |
| `noPersonne` | client ID             |
| `motDePasse` | client plain password |

If the authentication fails, you'll get an `CM0001` error code. See
[Errors](#errors).

Session
-------

The client must support HTTP cookies.

By sniffing the original application, you can see a `SessionId` in all
requests and responses after the authentication, but the session will be
destroyed if not using HTTP cookies. Note in some requests (but not all),
you have to provide the `SessionId` back in the request params. I advise you
to do it everytime since the original client does this too.

Errors
------

When an error occurs, the `Action` parameter is set to `Error`, and you get
`Code` and `ErrMsg` parameters, representing respectively the error code
and the error message.

### Known codes

| Code     | Description                                      |
| -------- | ------------------------------------------------ |
| `C01`    | service temporarily unavailable                  |
| `CM0001` | wrong credentials                                |
| `AT0008` | session expired, the login step must be replayed |

Methods
-------

### Cards

Get the list of active real cards for this account.

#### Request

| Name      | Value            |
| --------- | ---------------- |
| `Request` | `GetActiveCards` |
| `CardType`|                  |
| `VCardId` |                  |
| `codeEFS` | `21`             |
| `codeSi`  | `001`            |

#### Response

See [Arrays](#arrays).

| Name                | Type           | Description |
| ------------------- | -------------- | ----------- |
| `Total`             |                |             |
| `AdFrequency[x]`    | integer        |             |
| `CPN_Service[x]`    | boolean        |             |
| `CardType[x]`       | integer        |             |
| `VCardId[x]`        | integer        |             |
| `CardholderName[x]` | string         | holder name |
| `DefaultCard[x]`    | yes/no         |             |
| `Nickname[x]`       | string         | card name   |
| `PAN[x]`            | string         | card number |
| `VBV_Service[x]`    | string boolean |             |

### Virtual cards

Get the list of active virtual cards behind real card identified by
`CardType` and `VCardID`.

#### Request

See [Pagination](#pagination).

| Name       | Value                  |
| ---------- | ---------------------- |
| `Request`  | `GetActiveAccounts`    |
| `Start`    |                        |
| `Next`     |                        |
| `CardType` | previous `CardType[x]` |
| `VCardId`  | previous `VCardId[x]`  |

#### Response

See [Pagination](#pagination).
See [Arrays](#arrays).

| Name                  | Type       | Description                       |
| --------------------- | ---------- | --------------------------------- |
| `Start`               |            |                                   |
| `End`                 |            |                                   |
| `RecordCount`         |            |                                   |
| `Total`               |            |                                   |
| `AVV[x]`              | string     | secret code                       |
| `AuthAmount[x]`       | money      | ceiling                           |
| `CPNType[x]`          |            |                                   |
| `CumulativeLimit[x]`  | money      | ceiling                           |
| `UCumulativeLimit[x]` | float      | ceiling                           |
| `Currency[x]`         | integer    |                                   |
| `Expiry[x]`           | short date | expiry date                       |
| `StartDate[x]`        | short date | creation date                     |
| `IssueDate[x]`        | date       |                                   |
| `MerchantId[x]`       | string     |                                   |
| `MerchantName[x]`     |            |                                   |
| `NumUsage[x]`         | integer    | number of times the card was used |
| `OpenToBuy[x]`        | money      |                                   |
| `UOpenToBuy[x]`       | float      |                                   |
| `PAN[x]`              | string     | card number                       |
| `ValidFrom[x]`        | date       |                                   |

### Create card

Create a virtual card, with an amount ceiling (`CumulativeLimit`), and a
number of months the card will be valid (`ValidFor`), behind a real
card identified by `CardType` and `VCardID`.

#### Request

<table>
  <thead>
    <tr>
      <th>Name</th>
      <th>Type</th>
      <th>Description</th>
      <th>Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>Request</code></td>
      <td></td>
      <td></td>
      <td><code>GetCPN</code></td>
    </tr>
    <tr>
      <td><code>TransLimit</code></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td><code>CumulativeLimit</code></td>
      <td>integer</td>
      <td>ceiling</td>
      <td></td>
    </tr>
    <tr>
      <td><code>ValidFor</code></td>
      <td>integer</td>
      <td>months the card will be valid</td>
      <td></td>
    </tr>
    <tr>
      <td><code>CPNType</code></td>
      <td></td>
      <td></td>
      <td><code>SP</code></td>
    </tr>
    <tr>
      <td><code>CardType</code></td>
      <td></td>
      <td></td>
      <td>previous <code>CardType[x]</code></td>
    </tr>
    <tr>
      <td><code>VCardId</code></td>
      <td></td>
      <td></td>
      <td>previous <code>VCardId[x]</code></td>
    </tr>
  </tbody>
</table>

#### Response

| Name          | Type       | Description  |
| ------------- | ---------- | ------------ |
| `AVV`         | string     | secret code  |
| `Expiry`      | short date | expiry date  |
| `ExpiryMonth` | integer    | expiry month |
| `ExpiryYear`  | integer    | expiry year  |
| `From`        | short date |              |
| `PAN`         | string     | card number  |

### Delete card

Delete a virtual card identified by `CPNPAN`, owned by a real card
identified by `CardType` and `VCardID`.

#### Request

| Name       | Value                  |
| ---------- | ---------------------- |
| `Request`  | `CancelCPN`            |
| `CPNPAN`   | previous `PAN[x]`      |
| `CardType` | previous `CardType[x]` |
| `VCardId`  | previous `VCardId[x]`  |

#### Response

If there is no error, the response won't contain anything else than the
[Common response parameters](#common-response-parameters).

### Profiles list

#### Request

| Name          | Value                  |
| ------------- | ---------------------- |
| `Request`     | `ListProfileIds`       |
| `ProfileType` |                        |
| `CardType`    | previous `CardType[x]` |
| `VCardId`     | previous `VCardId[x]`  |

#### Response

See [Arrays](#arrays).

| Name             | Type   |
| ---------------- | ------ |
| `Total`          |        |
| `ProfileName[x]` | string |
| `ProfileType[x]` | string |

### Shipping profile

#### Request

| Name          | Value                     |
| ------------- | ------------------------- |
| `Request`     | `GetShippingProfile`      |
| `ProfileName` | previous `ProfileName[x]` |
| `CardType`    | previous `CardType[x]`    |
| `VCardId`     | previous `VCardId[x]`     |

#### Response

| Name               |
| ------------------ |
| `AdditionalField1` |
| `AdditionalField2` |
| `AdditionalField3` |
| `AdditionalField4` |
| `AdditionalField5` |
| `AdditionalField6` |
| `AdditionalField7` |
| `Address1`         |
| `Address2`         |
| `Address3`         |
| `Building`         |
| `City`             |
| `Country`          |
| `EmailAddress`     |
| `FirstName`        |
| `LastName`         |
| `MiddleName`       |
| `PhoneNumber1`     |
| `PhoneNumber2`     |
| `PhoneNumber3`     |
| `Postcode`         |
| `PrefixName`       |
| `ProfileName`      |
| `ProfileType`      |
| `StateProvince`    |
| `Status`           |
| `SuffixName`       |

### Buyings

#### Request

See [Pagination](#pagination).

| Name       | Type    | Value                  |
| ---------- | --------| ---------------------- |
| `Request`  |         | `GetPastTransactions`  |
| `Start`    |         |                        |
| `Next`     |         |                        |
| `CardType` |         | previous `CardType[x]` |
| `VCardId`  |         | previous `VCardId[x]`  |

#### Response

See [Pagination](#pagination).
See [Arrays](#arrays).

| Name                   | Type       | Description                       |
| ---------------------- | ---------- | --------------------------------- |
| `Start`                |            |                                   |
| `End`                  |            |                                   |
| `RecordCount`          |            |                                   |
| `Total`                |            |                                   |
| `AVV[x]`               | string     | secret code                       |
| `AuthCode[x]`          |            |                                   |
| `CPNType[x]`           |            |                                   |
| `CumulativeLimit[x]`   | money      | ceiling                           |
| `Currency[x]`          | integer    |                                   |
| `ExpiryDate[x]`        | short date | expiry date                       |
| `IssueDate[x]`         | date       |                                   |
| `MerchantCity[x]`      |            |                                   |
| `MerchantCountry[x]`   |            |                                   |
| `MerchantName[x]`      |            |                                   |
| `MicroRefNumber[x]`    |            |                                   |
| `NumUsage[x]`          | integer    | number of times the card was used |
| `OriginalAmount[x]`    | money      | same as `CumulativeLimit[x]`      |
| `PAN[x]`               | string     | card number                       |
| `Status[x]`            |            |                                   |
| `TransactionAmount[x]` | money      | transaction amount                |
| `TransactionDate[x]`   | money      | transaction date                  |
| `TransactionLimit[x]`  | money      | transaction limit                 |
| `UTransactionLimit[x]` | float      | transaction limit                 |
| `ValidFrom[x]`         | date       |                                   |
| `ValidTo[x]`           | date       |                                   |
