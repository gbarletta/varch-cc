# hello2.c
	
.sum:
	push	sf
	mov	sf, sp
	
	mov	r0, sf
	add	r0, 2
	mov	r1, [r0]
	mov	r0, sf
	add	r0, 4
	mov	r2, [r0]
	add	r1, r2
	mov	rv, r1
	mov	sp, sf
	pop	sf
	ret
.main:
	push	sf
	mov	sf, sp
	
	mov	r0, sum
	mov	r1, 2
	push	r1
	mov	r1, 2
	push	r1
	call	r0
	add	sf, 4
	mov	r0, rv
	mov	r1, sum
	mov	r2, 4
	push	r2
	mov	r2, 6
	push	r2
	call	r1
	add	sf, 4
	mov	r1, rv
	add	r0, r1
	mov	rv, r0
	mov	sp, sf
	pop	sf
	ret
