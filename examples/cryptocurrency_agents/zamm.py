import os
from ambientagi.services.agent_service import AmbientAgentService

# 1️⃣  Bootstrap the service (scheduler not needed here)
service = AmbientAgentService(api_key=os.getenv("OPENAI_API_KEY"))

# 2️⃣  (Optional) create a DB-tracked agent so you have an agent_id for bookkeeping
agent = service.create_agent(
    agent_name="ZammDemo",
    private_key=os.getenv("ETH_PRIVATE_KEY"),  # never stored server-side
    description="Mints an ERC-6909 token and seeds liquidity via ZAMM"
)
print(agent)
agent_id = agent["agent_records"][0]["agent_id"]
print("✅ Agent created:", agent_id)

# ---------------------------------------------------------------------
# 3️⃣  Mint a fixed-supply ERC-6909 token on ZAMM
#
#    - supply and amounts are *strings* in wei
#    - uri can point to IPFS JSON describing the token
# ---------------------------------------------------------------------
FIXED_SUPPLY_WEI = str(1_000_000 * 10**18)          # 1 M tokens with 18 decimals
METADATA_URI     = "ipfs://Qm.../my_token_meta.json"

# token_resp = service.zamm_make_token(
#     supply=FIXED_SUPPLY_WEI,
#     uri=METADATA_URI,
#     private_key=os.getenv("ETH_PRIVATE_KEY")
# )
# print("🪙 Token mint response:", token_resp)

# ---------------------------------------------------------------------
# 4️⃣  (Optional) Mint AND create a liquidity pool in one shot
# ---------------------------------------------------------------------
MINT_AMOUNT_WEI = "1000000000000000"   # 1 quadrillion wei  = 0.001 tokens if the token uses 18 decimals
LIQ_ETH_WEI     = "100000000000000"    # 0.0001 ETH        = 0.0001 ETH        # 0.1 ETH of initial liquidity
SWAP_FEE_BPS     = 30                               # 0.30 %

=

liq_resp = service.zamm_make_liquid(
    mkrAmt=MINT_AMOUNT_WEI,
    liqAmt=LIQ_ETH_WEI,
    swapFee=SWAP_FEE_BPS,
    uri=METADATA_URI,
    private_key=os.getenv("ETH_PRIVATE_KEY")
)
print("💧 makeLiquid response:", liq_resp)
