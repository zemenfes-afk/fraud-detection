import pandas as pd
import numpy as np
import socket
import struct


def ip_to_int(ip):
    """Converts IPv4 string to integer."""
    try:
        return struct.unpack("!I", socket.inet_aton(ip))[0]
    except:
        return 0


def merge_fraud_with_countries(fraud_df, ip_df):
    """Maps IP addresses to countries using range lookup."""
    # Convert IP addresses to integers
    fraud_df['ip_int'] = fraud_df['ip_address'].apply(ip_to_int)

    # Sort for merge_asof
    fraud_df = fraud_df.sort_values('ip_int')
    ip_df = ip_df.sort_values('lower_bound_ip_address')

    # Perform range-based merge
    merged = pd.merge_asof(
        fraud_df,
        ip_df,
        left_on='ip_int',
        right_on='lower_bound_ip_address'
    )

    # Verify if IP falls within the upper bound
    merged['country'] = np.where(
        merged['ip_int'] <= merged['upper_bound_ip_address'],
        merged['country'],
        'Unknown'
    )
    return merged