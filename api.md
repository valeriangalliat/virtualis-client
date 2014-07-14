Virtualis API
=============

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
      <td><code>yes/no</code></td>
      <td><code>Y</code> or <code>N</code></td>
    </tr>
    <tr>
      <td><code>date</code></td>
      <td>
        <code>day/month/year</code>, 2 digits for day and month,
        4 for year
      </td>
    </tr>
    <tr>
      <td><code>short date</code></td>
      <td>2 digits for month and year</td>
    </tr>
    <tr>
      <td><code>money</code></td>
      <td>
        the first character is an URL encoded money symbol (like
        <code>%80</code> for <code>€</code>), followed by a float number
        with <code>.</code> as decimal separator
      </td>
    </tr>
    <tr>
      <td>string boolean</td>
      <td>whether the string is <code>true</code> or <code>false</code></td>
  </tbody>
</table>

### Arrays

Some requests returns array-like structures. This is done with a `Total`
(or `RecordCount`, I need to figure this out) response parameter, and
multiple parameters ending with an integer representing the offset.

Example:

    Total: 2
    Foo1: value
    Bar1: value
    Foo2: value
    Bar2: value

I'll write these parameters ending with the `[x]` sequence, meant to be
replaced with a number, from 0 to `Total`:

    Foo[x]
    Bar[x]

Common Request Parameters
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

Common Response Parameters
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
destroyed if not using HTTP cookies.

Pagination
----------

Some requests support pagination. This is done with additional parameters
in the request and the response:

### Request

| Name    | Type    | Description                                 |
| ------- | ------- | ------------------------------------------- |
| `Start` | integer | start offset (0 for the first page)         |
| `Next`  | integer | no idea... probably next page record number |

### Response

| Name          | Type    | Description                       |
| ------------- | ------- | --------------------------------- |
| `RecordCount` | integer | number of records in current set  |
| `Start`       | integer | same as `Start` request parameter |
| `Total`       | integer | total number of records           |

Errors
------

When an error occurs, the `Action` parameter is set to `Error`, and you get
`Code` and `ErrMsg` parameters, representing respectively the error code
and the error message.

### Known Codes

| Code     | Description                                      |
| -------- | ------------------------------------------------ |
| `C01`    | service temporarily unavailable                  |
| `CM0001` | wrong credentials                                |
| `AT0008` | session expired, the login step must be replayed |

Requests
--------

### Active Cards

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

| Name                | Type           | Description |
| ------------------- | -------------- | ----------- |
| `Total`             | integer        |             |
| `AdFrequency[x]`    | integer        |             |
| `CPN_Service[x]`    | boolean        |             |
| `CardType[x]`       | integer        |             |
| `VCardId[x]`        | integer        |             |
| `CardholderName[x]` | string         | holder name |
| `DefaultCard[x]`    | yes/no         |             |
| `Nickname[x]`       | string         | card name   |
| `PAN[x]`            | integer        | card number |
| `VBV_Service[x]`    | string boolean |             |

### Active Virtual Cards

Get the list of active virtual cards behind real card (identified by
`CardType` and `VCardID`.

#### Request

| Name       | Type    | Value                  |
| ---------- | --------| ---------------------- |
| `Request`  |         |`GetActiveAccounts`     |
| `Start`    | integer | `0` by default         |
| `Next`     | integer | `20` by default        |
| `CardType` |         | previous `CardType[x]` |
| `VCardId`  |         | previous `VCardId[x]`  |

#### Response

| Name                  | Type       | Description                       |
| --------------------- | ---------- | --------------------------------- |
| `End`                 | integer    |                                   |
| `RecordCount`         | integer    |                                   |
| `Start`               | integer    |                                   |
| `Total`               | integer    |                                   |
| `AVV1`                | integer    | secret code                       |
| `AuthAmount[x]`       | money      | ceiling                           |
| `CPNType[x]`          |            |                                   |
| `CumulativeLimit[x]`  | money      | ceiling                           |
| `UCumulativeLimit[x]` | float      | ceiling                           |
| `Currency[x]`         | integer    |                                   |
| `Expiry[x]`           | short date | expiry date                       |
| `StartDate[x]`        | short date | creation date                     |
| `IssueDate[x]`        | date       |                                   |
| `MerchantId[x]`       | integer    |                                   |
| `MerchantName[x]`     |            |                                   |
| `MicroRefNumber[x]`   |            |                                   |
| `NumUsage[x]`         | integer    | number of times the card was used |
| `OpenToBuy[x]`        | money      |                                   |
| `UOpenToBuy[x]`       | float      |                                   |
| `PAN[x]`              | integer    | card number                       |
| `ValidFrom[x]`        | date       |                                   |

### Delete Card

#### Request

| Name       | Value                  |
| ---------- | ---------------------- |
| `CPNPAN`   | previous `PAN[x]`      |
| `CardType` | previous `CardType[x]` |
| `VCardId`  | previous `VCardId[x]`  |
| `Request`  | `CancelCPN`            |

### Create Virtual Card

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
| `AVV`         | integer    | secret code  |
| `Expiry`      | short date | expiry date  |
| `ExpiryMonth` | integer    | expiry month |
| `ExpiryYear`  | integer    | expiry year  |
| `From`        | short date |              |
| `PAN`         | integer    | card number  |



### Profiles List

#### Request

| Name          | Value                  |
| ------------- | ---------------------- |
| `Request`     | `ListProfileIds`       |
| `ProfileType` |                        |
| `CardType`    | previous `CardType[x]` |
| `VCardId`     | previous `VCardId[x]`  |

#### Response

| Name             | Type    |
| ---------------- | ------- |
| `Total`          | integer |
| `ProfileName[x]` |         |
| `ProfileType[x]` |         |

### Shipping Profile

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

| Name       | Type    | Value                  |
| ---------- | --------| ---------------------- |
| `Request`  |         | `GetPastTransactions`  |
| `Start`    | integer | `0` by default         |
| `Next`     | integer | `20` by default        |
| `CardType` |         | previous `CardType[x]` |
| `VCardId`  |         | previous `VCardId[x]`  |

#### Response

| Name                   | Type       | Description                       |
| ---------------------- | ---------- | --------------------------------- |
| `End`                  | integer    |                                   |
| `RecordCount`          | integer    |                                   |
| `Start`                | integer    |                                   |
| `Total`                | integer    |                                   |
| `AVV1`                 | integer    | secret code                       |
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
| `PAN[x]`               | integer    | card number                       |
| `Status[x]`            |            |                                   |
| `TransactionAmount[x]` | money      | transaction amount                |
| `TransactionDate[x]`   | money      | transaction date                  |
| `TransactionLimit[x]`  | money      | transaction limit                 |
| `UTransactionLimit[x]` | float      | transaction limit                 |
| `ValidFrom[x]`         | date       |                                   |
| `ValidTo[x]`           | date       |                                   |
