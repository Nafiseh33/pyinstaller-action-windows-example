import json
import requests
from web3 import Web3
from bitcoinlib.wallets import HDWallet as BTCWallet
from tronpy import Tron
from solana.rpc.api import Client as SolanaClient
from solana.keypair import Keypair
from solana.transaction import Transaction
from solana.system_program import TransferParams, transfer
from mnemonic import Mnemonic

# 3x 12-word seed phrases
SIGNERS = [
    "tunnel cluster sleep acoustic south drum what insane cloth short assist cliff",
    "cotton mimic drip fall inquiry chaos material grab turtle name fatal about",
    "speed such flat define opera enact gun confirm power evolve excuse collect"
]

# Multisig addresses (per network)
BTC_SAFE_ADDRESS = [
    "bc1qmx4tujafdhwm7fdl89llmvzmfl2tm0ncvk6el6",
    "bc1q7qzvaqyx8t90xy3e3jrx5lmlgut5awkkrrlrlr",
    "bc1qq5t90xat7ldfzudxmjre45lfjqnr7tcp5hezdc"
]

ETH_SAFE_ADDRESS = [
    "0xEB5539C33543bA2C0f796D2b5e712134F81E5e3B",
    "0x4BBA8aeEcDa81Dc2e44D5472B4e423ed949037d8",
    "0xe5E9D6B3439FD123ABe7a9F0E9B2fB0A52A77916"
]

TRON_SAFE_ADDRESS = [
    "TJ6nt9ffAzRooZkBAWXDBmprZUCSon6m9W",
    "TWjSN34GGPZBUKx22LbBC5ffpcqZfREeay",
    "TXuJm1tnmrSd2Bd6dQhzbQNwHMNbPNPziD"
]

SOLANA_SAFE_ADDRESS = [
    "6RMHSr8jFS6QaFPNdFDGZnYbKFNiAgfVRZtLDoc64eAB",
    "5MJ9EZ35Akp8xuCbKGtsfVjMTAcrqCPiUTgDkshWjhec",
    "CPzePAcCW6Fm44CmaStxCo1DR31PyMft9bwFjPMFdbFs"
]


# REAL BTC TRANSFER
def transfer_btc(from_address, to_address, amount_btc):
    print("\n➡️ Sending BTC on Mainnet...")
    wallet = BTCWallet.create('TempWallet', keys=SIGNERS, network='bitcoin', witness_type='segwit', multisig_n=3, multisig_m=3, db_uri=None)
    tx = wallet.send_to(to_address, amount_btc, network_fee=1000)
    print(f"✅ BTC Tx Sent: {tx.txid}")


# REAL ETH TRANSFER
def transfer_eth(from_address, to_address, amount_eth):
    print("\n➡️ Sending ETH on Mainnet...")
    infura_url = "https://mainnet.infura.io/v3/3ffde1e3db2a4a4684aa6620f69fad5b"  # INFURA URL
    w3 = Web3(Web3.HTTPProvider(infura_url))  # Using INFURA URL
    account = w3.eth.account.from_mnemonic(SIGNERS[0])
    nonce = w3.eth.get_transaction_count(from_address)
    tx = {
        'nonce': nonce,
        'to': to_address,
        'value': w3.to_wei(amount_eth, 'ether'),
        'gas': 21000,
        'gasPrice': w3.to_wei('50', 'gwei')
    }
    signed_tx = w3.eth.account.sign_transaction(tx, account.key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f"✅ ETH Tx Sent: {w3.to_hex(tx_hash)}")


# REAL TRON TRANSFER
def transfer_tron(from_address, to_address, amount_trx):
    print("\n➡️ Sending TRON on Mainnet...")
    client = Tron()
    priv_key = client.generate_address_from_mnemonic(SIGNERS[0])['private_key']
    txn = (
        client.trx.transfer(from_address, to_address, int(amount_trx * 1_000_000))
        .memo("Multisig Transfer")
        .build()
        .sign(priv_key)
    )
    result = txn.broadcast().wait()
    print(f"✅ TRON Tx Sent: {result['txid']}")


# REAL SOLANA TRANSFER
def transfer_solana(from_address, to_address, amount_sol):
    print("\n➡️ Sending SOLANA on Mainnet...")
    solana_client = SolanaClient("https://api.mainnet-beta.solana.com")
    seed = Mnemonic("english").to_seed(SIGNERS[0])[:32]
    kp = Keypair.from_seed(seed)
    tx = Transaction().add(
        transfer(
            TransferParams(
                from_pubkey=kp.public_key,
                to_pubkey=to_address,
                lamports=int(amount_sol * 1_000_000_000),
            )
        )
    )
    res = solana_client.send_transaction(tx, kp)
    print(f"✅ SOL Tx Sent: {res['result']}")


# MAIN SELECTOR
if __name__ == "__main__":
    print("Select Network to Send:")
    print("1) BTC\n2) ETH\n3) TRON\n4) SOL")
    choice = input("Your choice: ")

    from_addr = input("From Address: ")
    to_addr = input("To Address: ")
    amount = float(input("Amount to Send: "))

    if choice == '1':
        transfer_btc(from_addr, to_addr, amount)
    elif choice == '2':
        transfer_eth(from_addr, to_addr, amount)
    elif choice == '3':
        transfer_tron(from_addr, to_addr, amount)
    elif choice == '4':
        transfer_solana(from_addr, to_addr, amount)
    else:
        print("❌ Invalid Choice")
