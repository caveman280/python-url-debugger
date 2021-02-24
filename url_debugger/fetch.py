import re
import time
import requests
import socket

from exceptions import *  # noqa

CURL_TIMEOUT = 10

class FetchUrl(object):
    def __init__(self, url: str, follow_redirects=True):
        self.url = url
        self._follow_redirect = follow_redirects
        self._has_performed_request = False
        self._has_critical_error = False
        self._errors = []
        self._request = None
        self._ip = None
        self._port = None
    
    def _valid_url(self) -> bool:
        """
        Perform a regex validation against the URL provided.
        """
        # Regex:
        ## (?i) = First, perform case insensitive matches
        # Regex Groups:
        ## 1st Group: (?:https?://)
        ### ?: = Non-capturing (the whole URL is a capture group, so don't capture this)
        ### https? = matches the s character 0 or 1 times (so http or https is valid)
        ## 2nd Group: (?:[a-z0-9][a-z0-9-]*\.[^\s]{2,})
        ### ?: = Non-capturing (the whole URL is a capture group, so don't capture this)
        ### [a-z0-9] = matches 1 character if it's a number of letter
        ### [a-z0-9-]* = matches any character if it's a number of letter or a dash zero or unlimited times
        ### \. = literally, a .
        #### [^\s] = matches anything which isn't a whitespace
        #### {2,} = repeat this group 2 or as many times as needed (takes into account subdomains)
        regex = r"(?i)((?:https?://)(?:[a-z0-9][a-z0-9-]*\.[^\s]{2,}))"
        return bool(re.match(regex, self.url))

    def fetch(self) -> None:
        """
        Provided that a valid URL has been provided when creating this class,
        this method will perform the GET request to the remote address.
        """
        if not self._valid_url():
            self._has_performed_request = True
            self._has_critical_error = True
            self._errors.append(InvalidUrl())
        else:
            try:
                with requests.get(self.url, timeout=CURL_TIMEOUT, stream=True, allow_redirects=self._follow_redirect) as rsp:
                    # raw._connection is lost after we consume the body
                    # extract ip & port before this!
                    # https://github.com/psf/requests/issues/2158#issuecomment-172446171
                    try:
                        self._ip, self._port = rsp.raw._connection.sock.getpeername()
                    except:
                        # we'll allow this to pass in case it fails
                        pass
                    self._request = rsp
            except Exception as e:
                self._has_critical_error = True
                #exception_type, exception_value, exception_traceback = sys.exc_info()
                self._errors.append(e)
            self._has_performed_request = True
            

    def as_dict(self) -> dict:
        """
        Return a dict type response describing this object.
        This includes describing any errors as strings.
        """
        r = dict()
        r["url"] = self.url
        if self._has_critical_error:
            r["errors"] = []
            for error in self._errors:
                r["errors"].append(str(error)) 
        else:
            if not self._has_performed_request:
                r["warning"] = "haven't sent request yet"
            else:
                if type(self._request) is requests.Response:
                    r["http_method"] = self._request.request.method
                    r["response_code"] = self._request.status_code
                    r["http_version"] = self._request.raw.version
                    r["headers"] = dict(
                        (k, v) for k, v in self._request.headers.items() if k not in "authorization"
                    )
                    if len(self._request.history) > 0:
                        # we've been redirected
                        r['redirect_count'] = len(self._request.history)
                        r['redirect_history'] = [request.url for request in self._request.history]
                    if self._ip is not None and self._port is not None:
                        r["remote_ip"] = self._ip
                        r["remote_port"] = self._port
        return r