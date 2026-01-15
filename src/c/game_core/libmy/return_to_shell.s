.arm
.section .text
.align 2
.global return_to_shell
.type return_to_shell, %function

return_to_shell:
    mov r1, #0x04000000     @ REG_BASE
    mov r0, #0

    @ --- DMA 全停止 ---
    strh r0, [r1, #0xBA]    @ DMA0CNT_H
    strh r0, [r1, #0xC6]    @ DMA1CNT_H
    strh r0, [r1, #0xD2]    @ DMA2CNT_H
    strh r0, [r1, #0xDE]    @ DMA3CNT_H

    @ --- IRQ 完全 OFF ---
    add r1, r1, #0x200
    str r0, [r1, #8]       @ IE = 0

    @ --- PogoShell / 互換フック確認 ---
    ldr     r1, =0x03007FFA
    ldrh    r2, [r1]
    cmp     r2, #0
    beq     do_softreset   @ フック無し → 通常リセット

    @ フックあり → メニューへジャンプ
    bx      r2

do_softreset:
    mov     r0, #0
    strh    r0, [r1]       @ 念のためクリア
    mov     r0, #8
    swi     0x010000       @ VRAM clear
    swi     0x000000       @ SoftReset

    b       .              @ 念のため
