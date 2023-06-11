# hello.c
	
.fibonacci:
	push	sf
	mov	sf, sp
	sub	sp, 0
	mov	r0, sf + 4
	mov	r1, [r0]
	mov	r0, 1
	cmp	r1, r0
	flg	r1, FLAGS_LESSEQ
	jnz	r1, L0
	jmp	L1
.L0:
	mov	r0, sf + 4
	mov	r1, [r0]
	mov	rv, r1
	jmp	L2
.L1:
	mov	r0, fibonacci
	mov	r1, sf + 4
	mov	r2, [r1]
	mov	r1, 1
	sub	r2, r1
	push	r2
	call	r0
	add	sf, 2
	mov	r0, rv
	mov	r1, fibonacci
	mov	r2, sf + 4
	mov	r3, [r2]
	mov	r2, 2
	sub	r3, r2
	push	r3
	call	r1
	add	sf, 2
	mov	r1, rv
	add	r0, r1
	mov	rv, r0
.L2:
	mov	sp, sf
	pop	sf
	ret
.main:
	push	sf
	mov	sf, sp
	mov	r0, fibonacci
	mov	r1, 10
	push	r1
	call	r0
	add	sf, 2
	mov	r0, rv
	mov	rv, r0
	mov	sp, sf
	pop	sf
	ret
