#: Operation ids
ops = [
    "transfer",
    "limit_order_create",
    "limit_order_cancel",
    "call_order_update",
    "fill_order",
    "account_create",
    "account_update",
    "account_whitelist",
    "account_upgrade",
    "account_transfer",
    "asset_create",
    "asset_update",
    "asset_update_bitasset",
    "asset_update_feed_producers",
    "asset_issue",
    "asset_reserve",
    "asset_fund_fee_pool",
    "asset_settle",
    "asset_global_settle",
    "asset_publish_feed",
    "proposal_create",
    "proposal_update",
    "proposal_delete",
    "withdraw_permission_create",
    "withdraw_permission_update",
    "withdraw_permission_claim",
    "withdraw_permission_delete",
    "committee_member_create",
    "committee_member_update",
    "committee_member_update_global_parameters",
    "vesting_balance_create",
    "vesting_balance_withdraw",
    "custom",
    "assert",
    "balance_claim",
    "override_transfer",
    "asset_settle_cancel",
    "asset_claim_fees",
    "bid_collateral",
    "execute_bid",
    "create_contract",
    "call_contract",
    "contract_transfer",
    "change_sidechain_config",
    "account_address_create",
    "transfer_to_address",
    "generate_eth_address",
    "create_eth_address",
    "deposit_eth",
    "withdraw_eth",
    "approve_withdraw_eth",
    "contract_fund_pool",
    "contract_whitelist",
    "sidechain_issue",
    "sidechain_burn",
    "register_erc20_token",
    "deposit_erc20_token",
    "withdraw_erc20_token",
    "approve_erc20_token_withdraw",
    "contract_update"
]
operations = {o: ops.index(o) for o in ops}
