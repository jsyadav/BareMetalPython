import oraclebmc

def verify_syntax(addressToVerify):
    import re
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', addressToVerify)

    if match == None:
        print('Bad Syntax')
        raise ValueError('Bad Syntax')
    else:
        return True

def get_mx_record(domain):

    import dns.resolver
    records = dns.resolver.query(domain, 'MX')
    for r in records:
        print(r.exchange)
    mxRecord = records[0].exchange
    mxRecord = str(mxRecord)
    print(mxRecord)
    return mxRecord

def validateEmail(addressToVerify):
    import socket
    import smtplib
    from email_split import email_split

    # Get local server hostname
    host = socket.gethostname()

    # SMTP lib setup (use debug level for full output)
    server = smtplib.SMTP()
    server.set_debuglevel(0)


    # SMTP Conversation
    email_domain = email_split(addressToVerify).domain
    #mxRecord = get_mx_record(email_domain)
    server.connect('aserp2030.oracle.com')

    # exchanger ='aserp1040.oracle.com'
    # exchanger = userv0021.oracle.com
    # exchanger = aserv0021.oracle.com
    # exchanger = aserv0022.oracle.com
    # exchanger = 'userv0022.oracle.com'
    #server.connect(exchanger)
    server.helo(host)
    server.mail('jitendra.yadav@oracle.com')
    code, message = server.rcpt(str(addressToVerify),options=[])
    #print (code, message)
    server.quit()

    # Assume 250 as Success
    if code == 250:
        #print('Success')
        #print(addressToVerify, ' is valid')
        return True
    else:
        #print('Bad')
        print(addressToVerify, ' is invalid <<<<<<')
        return False


def find_invalid_user():
    config = oraclebmc.config.from_file("bmc_config", "DEFAULT")
    identity = oraclebmc.identity.IdentityClient(config)

    def paginate(operation, *args, **kwargs):
        while True:
            response = operation(*args, **kwargs)
            for value in response.data:
                yield value
            kwargs["page"] = response.next_page
            if not response.has_next_page:
                break

    for user in paginate(identity.list_users, compartment_id=config['tenancy']):
        validateEmail(user.name)


if __name__ == "__main__":
    addressToVerify = 'steve.griffin@oracle.com'
    addressToVerify = 'jessica.mao@oracle.com'
    # is_valid = verify_syntax(addressToVerify)
    # print(is_valid)
    is_valid = validateEmail(addressToVerify)
    print(is_valid)
    find_invalid_user();