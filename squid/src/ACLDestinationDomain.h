
/*
 * $Id: ACLDestinationDomain.h,v 1.8 2005/05/09 01:41:25 hno Exp $
 *
 *
 * SQUID Web Proxy Cache          http://www.squid-cache.org/
 * ----------------------------------------------------------
 *
 *  Squid is the result of efforts by numerous individuals from
 *  the Internet community; see the CONTRIBUTORS file for full
 *  details.   Many organizations have provided support for Squid's
 *  development; see the SPONSORS file for full details.  Squid is
 *  Copyrighted (C) 2001 by the Regents of the University of
 *  California; see the COPYRIGHT file for full details.  Squid
 *  incorporates software developed and/or copyrighted by other
 *  sources; see the CREDITS file for full details.
 *
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2 of the License, or
 *  (at your option) any later version.
 *  
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *  
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111, USA.
 *
 *
 * Copyright (c) 2003, Robert Collins <robertc@squid-cache.org>
 */

#ifndef SQUID_ACLSOURCEDOMAIN_H
#define SQUID_ACLSOURCEDOMAIN_H
#include "ACL.h"
#include "ACLData.h"
#include "ACLChecklist.h"
#include "ACLStrategised.h"

class ACLDestinationDomainStrategy : public ACLStrategy<char const *>
{

public:
    virtual int match (ACLData<MatchType> * &, ACLChecklist *);
    static ACLDestinationDomainStrategy *Instance();
    /* Not implemented to prevent copies of the instance. */
    /* Not private to prevent brain dead g+++ warnings about
     * private constructors with no friends */
    ACLDestinationDomainStrategy(ACLDestinationDomainStrategy const &);

private:
    static ACLDestinationDomainStrategy Instance_;
    ACLDestinationDomainStrategy(){}

    ACLDestinationDomainStrategy&operator=(ACLDestinationDomainStrategy const &);
};

class DestinationDomainLookup : public ACLChecklist::AsyncState
{

public:
    static DestinationDomainLookup *Instance();
    virtual void checkForAsync(ACLChecklist *)const;

private:
    static DestinationDomainLookup instance_;
    static void LookupDone(const char *, void *);
};

class ACLDestinationDomain
{

private:
    static ACL::Prototype LiteralRegistryProtoype;
    static ACLStrategised<char const *> LiteralRegistryEntry_;
    static ACL::Prototype RegexRegistryProtoype;
    static ACLStrategised<char const *> RegexRegistryEntry_;
};

#endif /* SQUID_ACLSOURCEDOMAIN_H */
