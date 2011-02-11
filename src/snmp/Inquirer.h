/*
 * $Id$
 *
 * DEBUG: section 49    SNMP Interface
 *
 */

#ifndef SQUID_SNMPX_INQUIRER_H
#define SQUID_SNMPX_INQUIRER_H

#include "ipc/Inquirer.h"
#include "snmp/forward.h"
#include "snmp/Pdu.h"


class CommCloseCbParams;

namespace Snmp
{

/// Coordinator's job that sends a PDU request to each strand,
/// aggregates strand responses and send back the result to client
class Inquirer: public Ipc::Inquirer
{
public:
    Inquirer(const Request& aRequest, const Ipc::StrandCoords& coords);

protected:
    /* AsyncJob API */
    virtual void start();
    virtual bool doneAll() const;

    /* Ipc::Inquirer API */
    virtual void cleanup();
    virtual void handleException(const std::exception& e);
    virtual void sendResponse();
    virtual bool aggregate(Ipc::Response::Pointer aResponse);

private:
    void noteCommClosed(const CommCloseCbParams& params);

private:
    Pdu aggrPdu; ///< aggregated pdu
    int fd; ///< client connection descriptor

    AsyncCall::Pointer writer; ///< comm_write callback
    AsyncCall::Pointer closer; ///< comm_close handler

    CBDATA_CLASS2(Inquirer);
};

} // namespace Snmp

#endif /* SQUID_SNMPX_INQUIRER_H */
