import pandas as pd

data = pd.read_csv('combined_data.csv')

weapons = ['Staff', 'Shotgun', 'Hammer', 'Sword']

weapon_stats = {}
for w in weapons:
    attack_col = f'{w}_AttackCount'
    damage_col = f'{w}_TotalDamage'
    dps_col = f'{w}_DPS'
    skill_count_col = f'{w}_WSkillCount'

    total_attacks = data[attack_col].sum()
    total_damage = data[damage_col].sum()
    total_skill_uses = data[skill_count_col].sum()

    dps_nonzero = data.loc[data[attack_col] > 0, dps_col]
    avg_dps = dps_nonzero.mean() if not dps_nonzero.empty else 0

    weapon_stats[w] = {
        'TotalAttacks': total_attacks,
        'TotalDamage': total_damage,
        'AvgDPS': avg_dps,
        'TotalSkillUses': total_skill_uses,
    }

weapon_df = pd.DataFrame(weapon_stats).T
print("=== 무기별 종합 성능 ===")
print(weapon_df)

difficulty_by_segment = data.groupby('SegmentNumber').apply(
    lambda g: (g['DamageReceivedByEnemy'] / g['PlayTime']).mean()
).reset_index(name='AvgDamagePerSecond')

hard_segments = difficulty_by_segment.sort_values(by='AvgDamagePerSecond', ascending=False).head(10)

print("\n=== 구간별 난이도 상위 10개 ===")
print(hard_segments)

weapon_df.to_csv('weapon_performance_summary.csv')
hard_segments.to_csv('top10_hard_segments.csv', index=False)
