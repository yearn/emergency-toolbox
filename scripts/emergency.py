from ape_safe import ApeSafe
from brownie import ZERO_ADDRESS

def vault_shutdown():
    """
    @notice
        Can be called by gov or guardian
    """

    safe = ApeSafe('ychad.eth')
    vault = safe.contract('0xa258C4606Ca8206D8aA700cE2143D7db854D168c')
    vault.setEmergencyShutdown(True)

    safe_tx = safe.multisend_from_receipts()
    safe.preview(safe_tx, call_trace=False)
    safe.post_transaction(safe_tx)


def vault_revoke_and_harvest_all():
    safe = ApeSafe('ychad.eth')
    vault = safe.contract('0xa258C4606Ca8206D8aA700cE2143D7db854D168c')

    for i in range(0, 20):
        strat_address = vault.withdrawalQueue(i)
        if strat_address == ZERO_ADDRESS:
            break

        strat = safe.contract(strat_address)
        vault.revokeStrategy(strat)
        strat.harvest()

    # In case there is dust
    assert vault.totalDebt() < Wei("0.01 ether")

    safe_tx = safe.multisend_from_receipts()
    safe.preview(safe_tx, call_trace=False)
    safe.post_transaction(safe_tx)
