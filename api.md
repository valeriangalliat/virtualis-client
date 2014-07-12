Virtualis API
=============

Format
------

All the API calls are made with HTTPS protocol, using the `POST` HTTP method
with path `/cvd/WebServlet`, on `www.service-virtualis.com` host.

All `POST` HTTP requests are in `application/x-www-form-urlencoded` content
type, and the response body is in the same format.

The request data must be encoded in ISO-8859-1, and the returned data
is in the same encoding.

Do not trust the `Content-Type` header at all. They always set it to
`text/html; charset=UTF-8` even if they're actually sending
`application/x-www-form-urlencoded; charset=ISO-8859-1`.

All urlencoded responses can contain a trailing `&`, or multiple `&` (empty
parameter). In a strict parsing, you should remove them first.

All urlencoded cannot contain any array parameter, you can assume each
parameter is unique.

Session
-------

The client must support HTTP cookies. A `SessionId` is also given in HTTP
responses, but if you pass it again in the request body, it is ignored
(even if the original application always passes it both ways).

Authentication
--------------

For the first request (when you have no cookie, nor `SessionId`), you
have to append these parameters to the request body:

| Name         | Description           |
| ------------ | --------------------- |
| `noPersonne` | client ID             |
| `motDePasse` | client plain password |

If the authentication fails, you'll get an `CM0001` error code. See
[Errors](#errors) for more informations.

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
        client locale, two letter country code (like <code>fr</code>,
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
        can set it to `true` if you want to troll their browser statistics
      </td>
      <td></td>
    </tr>
    <tr>
      <td><code>startTime</code></td>
      <td>integer</td>
      <td>maybe the time since last request... `0` seems to be valid</td>
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

Errors
------

When an error occurs, the response `Action` parameter is set to `Error`,
with `Code` and `ErrMsg` parameters, representing respectively the error
code and the error message.

### Known Codes

| Code     | Description                                      |
| -------- | ------------------------------------------------ |
| `C01`    | service temporarily unavailable                  |
| `CM0001` | wrong credentials                                |
| `AT0008` | session expired, the login step must be replayed |

Arrays
------

Some requests returns arrays. This is done with a `Total` response parameter,
and multiple parameters ending with an integer representing the offset.

Example:

    Total: 2
    Foo1: value
    Bar1: value
    Foo2: value
    Bar2: value

I'll write these parameters ending with the `[x]` sequence, meant to be
replaced with a number, from 0 to `Total` range.

Types
-----

Some data types string formats are common in multiple parameters and are
described here.

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

Requests
--------

### Authentication & Active Cards

#### Request

| Name      | Type    | Description | Value            |
| --------- | ------- | ----------- | ---------------- |
| `Request` |         |             | `GetActiveCards` |
| `CardType`| unknown |             |                  |
| `VCardId` | unknown |             |                  |
| `codeEFS` |         |             | `21`             |
| `codeSi`  |         |             | `001`            |

#### Response

| Name                | Type           |
| ------------------- | -------------- |
| `Total`             | integer        |
| `AdFrequency[x]`    | integer        |
| `CPN_Service[x]`    | boolean        |
| `CardType[x]`       | integer        |
| `VCardId[x]`        | integer        |
| `CardholderName[x]` | string         |
| `DefaultCard[x]`    | yes/no         |
| `Nickname[x]`       | string         |
| `PAN[x]`            | integer        |
| `VBV_Service[x]`    | string boolean |

### Profiles List

#### Request

| Name          | Type    | Value                  |
| ------------- | ------- | ---------------------- |
| `Request`     |         | `ListProfileIds`       |
| `ProfileType` |         |                        |
| `CardType`    |         | previous `CardType[x]` |
| `VCardId`     |         | previous `VCardId[x]`  |

#### Response

| Name            | Type    |
| --------------- | ------- |
| `Total`         | integer |
| `ProfileName[x] |         |
| `ProfileType[x] |         |

### Shipping Profile

#### Request

| Name          | Type   | Value                     |
| ------------- | ------ | ------------------------- |
| `Request`     | string | `GetShippingProfile`      |
| `ProfileName` |        | previous `ProfileName[x]` |
| `CardType`    |        | previous `CardType[x]`    |
| `VCardId`     |        | previous `VCardId[x]`     |

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
      <td>GetCPN</td>
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
      <td>maximum amount to credit</td>
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

| Name          | Type       | Description     |
| ------------- | ---------- | --------------- |
| `AVV`         | integer    | secret code     |
| `Expiry`      | short date | expiration date |
| `ExpiryMonth` | integer    |                 |
| `ExpiryYear`  | integer    |                 |
| `From`        | short date |                 |
| `PAN`         | integer    | card number     |

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
| `CumulativeLimit[x]`   | money      | maximum debit                     |
| `Currency[x]`          | integer    |                                   |
| `ExpiryDate[x]`        | short date | expiration date                   |
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

### Active Cards

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
| `RecordCount`         | integer    | number of records                 |
| `Start`               | integer    |                                   |
| `Total`               | integer    |                                   |
| `AVV1`                | integer    | secret code                       |
| `AuthAmount[x]`       | money      | maximum debit                     |
| `CPNType[x]`          |            |                                   |
| `CumulativeLimit[x]`  | money      | maximum debit                     |
| `UCumulativeLimit[x]` | float      | maximum debit                     |
| `Currency[x]`         | integer    |                                   |
| `Expiry[x]`           | short date | expiration date                   |
| `StartDate[x]`        | short date | created date                      |
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
