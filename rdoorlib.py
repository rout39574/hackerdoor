
# vim:ft=python:ai:expandtab:ts=4:



class GHCard:
    # This is the attribute byte, but only item defined is bit 0 == 1 is access allowed, 0 is denied
    access = None
    # facility code (FC)
    facility = None
    # card code (CC)
    card = None

    # if new ACL list says we are denied
    set_denied = False
    # if new ACL list says we are allowed
    set_allowed = False
    # if matches new ACL list entry
    no_change = False
    # if processed in new ACL list
    done = False

    def __init__( self, access, facilityCode, cardCode ):
        self.access = access
        self.fc = facilityCode
        self.cc = cardCode

    def __eq__( self, other ):
        if type(self) is type(other):
            return self.facility == other.facility and self.card == other.card
        else:
            return False

class GHACL:
    acl = None

    def __init__( self, acl=None ):
        if acl is None:
            acl = []
        self.acl = acl

    def add( self,  card ):
        self.acl.append( card )

    def deltaListTo( self, gold ):
        add = []
        # n is new card
        for n in gold.acl:
            # o is old
            newCard = True
            for o in self.acl:
                # if o.done == True: # WTF? duplicate new card data in gold? XXX
                # How generate error here
                if n == o:
                    newCard = False
                    if o.access != n.access:
                        if n.access:
                            o.set_denied = True
                        else:
                            o.set_allowed = True
                    else:
                        o.no_change = True
                n.done = True
                o.done = True
            if newCard and n.access:
                n.done = True
                add.append( n )
        for o in self.acl:
            if o.done:
                continue
            if o.access:
                # no card matched in new ACL list, disable it
                o.set_denied = True
