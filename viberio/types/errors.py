class ViberBaseError(Exception):
    code = 0
    message = 'ok'

    def __init__(self, status_message, data):
        self.status_message = status_message
        self.data = data

    def __str__(self):
        return f"{self.message}: {self.status_message}"

    @classmethod
    def check(cls, result: dict):
        code = result.get('status', None)
        if code != 0:
            # raise cls(result['status_message'], result['status'], result)
            exc = ERRORS.get(code, GeneralError)
            raise exc(result['status_message'], result)
        return True


class InvalidUrl(ViberBaseError):
    message = "The webhook URL is not valid"
    code = 1


class InvalidAuthToken(ViberBaseError):
    message = "The authentication token is not valid"
    code = 2


class BadData(ViberBaseError):
    message = "There is an error in the request itself (missing comma, brackets, etc.)"
    code = 3


class MissingData(ViberBaseError):
    message = "Some mandatory data is missing"
    code = 4


class ReceiverNotRegistered(ViberBaseError):
    message = "The receiver is not registered to Viber"
    code = 5


class ReceiverNotSubscribed(ViberBaseError):
    message = "The receiver is not subscribed to the account"
    code = 6


class PublicAccountBlocked(ViberBaseError):
    message = "The account is blocked"
    code = 7


class PublicAccountNotFound(ViberBaseError):
    message = "The account associated with the token is not a account."
    code = 8


class PublicAccountSuspended(ViberBaseError):
    message = "The account is suspended"
    code = 9


class webhookNotSet(ViberBaseError):
    message = "No webhook was set for the account"
    code = 10


class ReceiverNoSuitableDevice(ViberBaseError):
    message = "The receiver is using a device or a Viber version that don’t support accounts"
    code = 11


class TooManyRequests(ViberBaseError):
    message = "Rate control breach"
    code = 12


class ApiVersionNotSupported(ViberBaseError):
    message = "Maximum supported account version by all user’s devices is less than the minApiVersion in the message"
    code = 13


class IncompatibleWithVersion(ViberBaseError):
    message = "minApiVersion is not compatible to the message fields"
    code = 14


class PublicAccountNotAuthorized(ViberBaseError):
    message = "The account is not authorized"
    code = 15


class InchatReplyMessageNotAllowed(ViberBaseError):
    message = "Inline message not allowed"
    code = 16


class PublicAccountIsNotInline(ViberBaseError):
    message = "The account is not inline"
    code = 17


class NoPublicChat(ViberBaseError):
    message = "Failed to post to public account. The bot is missing a Public Chat interface"
    code = 18


class CannotSendBroadcast(ViberBaseError):
    message = "Cannot send broadcast message"
    code = 19


class BroadcastNotAllowed(ViberBaseError):
    message = "Attempt to send broadcast message from the bot"
    code = 20


class GeneralError(ViberBaseError):
    message = "General error"
    code = None


ERRORS = {
    InvalidUrl.code: InvalidUrl,
    InvalidAuthToken.code: InvalidAuthToken,
    BadData.code: BadData,
    MissingData.code: MissingData,
    ReceiverNotRegistered.code: ReceiverNotRegistered,
    ReceiverNotSubscribed.code: ReceiverNotSubscribed,
    PublicAccountBlocked.code: PublicAccountBlocked,
    PublicAccountNotFound.code: PublicAccountNotFound,
    PublicAccountSuspended.code: PublicAccountSuspended,
    webhookNotSet.code: webhookNotSet,
    ReceiverNoSuitableDevice.code: ReceiverNoSuitableDevice,
    TooManyRequests.code: TooManyRequests,
    ApiVersionNotSupported.code: ApiVersionNotSupported,
    IncompatibleWithVersion.code: IncompatibleWithVersion,
    PublicAccountNotAuthorized.code: PublicAccountNotAuthorized,
    InchatReplyMessageNotAllowed.code: InchatReplyMessageNotAllowed,
    PublicAccountIsNotInline.code: PublicAccountIsNotInline,
    NoPublicChat.code: NoPublicChat,
    CannotSendBroadcast.code: CannotSendBroadcast,
    BroadcastNotAllowed.code: BroadcastNotAllowed,
    GeneralError.code: GeneralError,
}
