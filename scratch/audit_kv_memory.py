import math
import sys

sys.stdout.reconfigure(encoding="utf-8")

# RTX 6000 Specs
VRAM_TOTAL_MB = 48 * 1024 # 49152 MB
VRAM_TOTAL_BYTES = 48 * (1024**3)

print("="*80)
print("SGLANG MEMORY & KV CACHE FORMAL AUDIT (RTX 6000 48GB)")
print("="*80)

# Memory fractions
for frac in [0.96, 0.88, 0.85]:
    allocated_mb = VRAM_TOTAL_MB * frac
    headroom_mb = VRAM_TOTAL_MB * (1.0 - frac)
    print(f"\nFraction: {frac:.2f}")
    print(f"  Static Pool Allocated: {allocated_mb:.1f} MB ({allocated_mb/1024:.2f} GB)")
    print(f"  Dynamic Headroom:      {headroom_mb:.1f} MB ({headroom_mb/1024:.2f} GB)")

# Model Architecture for Qwen3.8 Flash-Next
# Qwen3.8 Flash-Next has hybrid Attention + Linear/Mamba layers.
# Standard Transformer Attention layers: typically 24-28 layers with GQA.
# Suppose num_layers = 28, num_key_value_heads = 4, head_dim = 128.
# (If 8 KV heads: 8 * 128 = 1024 per layer).
# In FP8 (1 byte per element):
# KV cache per token per layer = 2 (K and V) * num_kv_heads * head_dim * 1 byte.
# For num_kv_heads = 4, head_dim = 128: 2 * 4 * 128 * 1 = 1,024 bytes/token/layer.
# Across 28 layers: 28 * 1,024 = 28,672 bytes/token (~28 KB/token).
# In BF16 (2 bytes per element): ~56 KB/token.
# In FP8: ~28 KB/token.

# Let's test different KV cache bytes per token:
for kv_heads, layers, h_dim in [(4, 28, 128), (8, 28, 128), (4, 32, 128)]:
    bytes_per_tok_fp8 = 2 * kv_heads * h_dim * layers * 1 # 1 byte for fp8_e4m3
    bytes_per_tok_bf16 = 2 * kv_heads * h_dim * layers * 2
    print(f"\nConfig (heads={kv_heads}, layers={layers}, dim={h_dim}):")
    print(f"  FP8 KV Cache per token:  {bytes_per_tok_fp8:,} bytes ({bytes_per_tok_fp8/1024:.1f} KB)")
    print(f"  BF16 KV Cache per token: {bytes_per_tok_bf16:,} bytes ({bytes_per_tok_bf16/1024:.1f} KB)")
    
    # Under mem-fraction 0.88:
    # Model weights ~19.5 GB (INT4 base + FP8 draft + PLE)
    weight_gb = 19.5
    avail_kv_gb_88 = (VRAM_TOTAL_MB * 0.88 / 1024) - weight_gb
    avail_kv_bytes_88 = avail_kv_gb_88 * (1024**3)
    tokens_fp8 = int(avail_kv_bytes_88 / bytes_per_tok_fp8)
    print(f"  At mem-fraction 0.88 (Avail KV: {avail_kv_gb_88:.2f} GB):")
    print(f"    Total FP8 KV Cache Capacity: {tokens_fp8:,} tokens")
    print(f"    Concurrent 58k context streams: {tokens_fp8 / 58000:.2f} streams")
    print(f"    Concurrent 10-request active concurrency at avg 30k tokens: {tokens_fp8 / (10 * 30000):.2f}x capacity")

