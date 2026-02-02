"""
诊断模块：基于 explore/validate 指标、门禁状态、样本量、OS 结果，
输出 failure_type、primary_signal、next_action。
供 Summary 与「下一步变体建议」使用，替代泛泛的「复测」。
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

MIN_SAMPLES = 6
MIN_WINDOWS = 3


@dataclass
class DiagnosisResult:
    """诊断输出：failure_type, primary_signal, next_action"""

    failure_type: str = "inconclusive"  # inconclusive | handoff | structure | os_divergence
    primary_signal: str = ""  # IPM_drop | CPI_spike | ROAS_drop | sample_low | -
    next_action: str = "补样本"  # 补样本 | 换hook | 换触发 | 补证据 | 改承接 | 放量
    detail: str = ""


def diagnose(
    *,
    explore_ios: Any = None,
    explore_android: Any = None,
    validate_result: Any = None,
    metrics: list[Any] | None = None,
    windowed_metrics: list[Any] | None = None,
) -> DiagnosisResult:
    """
    诊断：输入 explore/validate 指标、门禁状态、样本量、OS 结果，
    输出 failure_type、primary_signal、next_action。

    failure_type:
    - inconclusive: 样本不足，无法下结论
    - handoff: Explore 过但 Validate 未过，承接/跨窗问题
    - structure: Explore 未过，结构暂不成立
    - os_divergence: iOS 与 Android 结果不一致

    next_action:
    - 补样本 / 换hook / 换触发 / 补证据 / 改承接 / 放量
    """
    metrics = metrics or []
    n_samples = len([m for m in metrics if not getattr(m, "baseline", False)])
    detail_rows = getattr(validate_result, "detail_rows", None) or []
    n_windows = len(detail_rows)

    exp_ios_pass = (
        getattr(explore_ios, "gate_status", "") == "PASS" if explore_ios else False
    )
    exp_android_pass = (
        getattr(explore_android, "gate_status", "") == "PASS" if explore_android else False
    )
    val_pass = (
        getattr(validate_result, "validate_status", "") == "PASS" if validate_result else False
    )
    sm = getattr(validate_result, "stability_metrics", None)
    risk_notes = list(getattr(validate_result, "risk_notes", None) or [])

    # 1. 样本不足 → inconclusive
    if n_samples < MIN_SAMPLES or n_windows < MIN_WINDOWS:
        return DiagnosisResult(
            failure_type="inconclusive",
            primary_signal="sample_low",
            next_action="补样本",
            detail=f"样本 n={n_samples} 或窗口={n_windows} 不足，无法下结论",
        )

    # 2. 全部通过且稳定 → 放量
    if exp_ios_pass and exp_android_pass and val_pass:
        ipm_cv = getattr(sm, "ipm_cv", 1.0) if sm else 1.0
        if ipm_cv < 0.05:
            return DiagnosisResult(
                failure_type="",
                primary_signal="-",
                next_action="放量",
                detail="跨窗稳定、OS 一致、指标达线，结构成立",
            )
        # 门禁过但波动大 → 补证据
        return DiagnosisResult(
            failure_type="handoff",
            primary_signal="IPM_drop",
            next_action="补证据",
            detail="门禁通过但 IPM 波动大，建议延长观察补足稳定性证据",
        )

    # 3. OS 分歧 → os_divergence
    if exp_ios_pass != exp_android_pass:
        which_fail = "Android" if not exp_android_pass else "iOS"
        return DiagnosisResult(
            failure_type="os_divergence",
            primary_signal="os_split",
            next_action="补证据",
            detail=f"{which_fail} Explore 未过，双端结果不一致，需补足该端样本",
        )

    # 4. Explore 未过 → structure（结构不成立）
    if not exp_ios_pass and not exp_android_pass:
        # 从 risk_notes 推断 primary_signal 与 next_action
        primary = "-"
        action = "换hook"
        if any("IPM" in n and "回撤" in n for n in risk_notes):
            primary = "IPM_drop"
            if any("Hook" in n or "强刺激" in n for n in risk_notes):
                action = "换hook"
            else:
                action = "换触发"
        elif any("CPI" in n for n in risk_notes):
            primary = "CPI_spike"
            action = "换触发"
        elif any("ROAS" in n or "early" in n.lower() for n in risk_notes):
            primary = "ROAS_drop"
            action = "改承接"
        return DiagnosisResult(
            failure_type="structure",
            primary_signal=primary,
            next_action=action,
            detail="Explore 未过，结构暂不成立",
        )

    # 5. Explore 过但 Validate 未过 → handoff（承接问题）
    if val_pass:
        # 理论上不会进这里（val_pass 已在上面处理）
        return DiagnosisResult(
            failure_type="",
            primary_signal="-",
            next_action="放量",
            detail="验证通过",
        )

    # Validate 未过
    primary = "-"
    action = "改承接"
    if sm:
        ipm_drop = getattr(sm, "ipm_drop_pct", 0) or 0
        cpi_inc = getattr(sm, "cpi_increase_pct", 0) or 0
        if ipm_drop > 20:
            primary = "IPM_drop"
            if any("Hook" in n or "强刺激" in n for n in risk_notes):
                action = "换hook"
            elif any("Why now" in n or "虚高" in n for n in risk_notes):
                action = "换触发"
            else:
                action = "改承接"
        elif cpi_inc > 15:
            primary = "CPI_spike"
            action = "改承接"
        else:
            primary = "ROAS_drop" if any("ROAS" in n or "转化" in n for n in risk_notes) else "IPM_drop"
            action = "补证据"

    return DiagnosisResult(
        failure_type="handoff",
        primary_signal=primary,
        next_action=action,
        detail="Explore 过但 Validate 未过，跨窗承接或稳定性不足",
    )
