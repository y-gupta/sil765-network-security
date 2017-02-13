#pragma once
#include <cstdio>
#include "key.h"
#include "fbox.h"

uint64_t initial_permutation_box(uint64_t in){
  static const char ip_table[] = {
    58,50,42,34,26,18,10,2,
    60,52,44,36,28,20,12,4,
    62,54,46,38,30,22,14,6,
    64,56,48,40,32,24,16,8,
    57,49,41,33,25,17,9,1,
    59,51,43,35,27,19,11,3,
    61,53,45,37,29,21,13,5,
    63,55,47,39,31,23,15,7
  };
  uint64_t out = 0;
  for(int i=0;i<64;i++){
    out |= ((in >> (64-ip_table[i])) & 1)<<(63-i);
  }
  return out;
}

uint64_t inv_initial_permutation_box(uint64_t in){
  static const char inv_ip_table[] = {
    40,8,48,16,56,24,64,32,
    39,7,47,15,55,23,63,31,
    38,6,46,14,54,22,62,30,
    37,5,45,13,53,21,61,29,
    36,4,44,12,52,20,60,28,
    35,3,43,11,51,19,59,27,
    34,2,42,10,50,18,58,26,
    33,1,41,9,49,17,57,25
  };
  uint64_t out = 0;
  for(int i=0;i<64;i++){
    out |= ((in >> (64-inv_ip_table[i])) & 1)<<(63-i);
  }
  return out;
}

uint64_t encrypt(uint64_t in, uint64_t key){ //key has 8 redundant parity bits
  printf("plain: %016lX\nkey:   %016lX\n",in,key);

  uint64_t LR = initial_permutation_box(in);
  uint32_t L, R, tmp;
  uint64_t K, CD; //CD is internal key_schedule state, K is the output key

  L = (LR >> 32) & 0xffffffff;
  R = LR & 0xffffffff;

  printf("00 - L: %08X  R: %08X\n",L,R);

  CD = key;
  for(int i=1;i<=16;i++){
    K = key_round(i, CD);
    tmp = L ^ fiestel_box(R, K);
    L = R;
    R = tmp;

    printf("%02d - L: %08X  R: %08X  K: %012lX  CD: %016lX\n",i,L,R,K,CD);
  }

  //swap L and R
  tmp = L;
  L = R;
  R = tmp;

  LR = (uint64_t(L) << 32) | R;

  printf("LR: %016lX\n",LR);
  LR = inv_initial_permutation_box(LR);
  printf("cipher: %016lX\n",LR);
  return LR;
}

uint64_t decrypt(uint64_t in, uint64_t key){ //key has 8 redundant parity bits
  printf("cipher: %016lX\nkey:   %016lX\n",in,key);

  uint64_t LR = initial_permutation_box(in);
  uint32_t L, R, tmp;
  uint64_t K, CD; //CD is internal key_schedule state, K is the output key

  L = (LR >> 32) & 0xffffffff;
  R = LR & 0xffffffff;

  tmp = L; L = R; R = tmp;

  printf("00 - L: %08X  R: %08X\n",L,R);

  CD = key;
  for(int i=1;i<=16;i++){
    K = inv_key_round(i, CD);
    tmp = R ^ fiestel_box(L, K);
    R = L;
    L = tmp;

    printf("%02d - L: %08X  R: %08X  K: %012lX  CD: %016lX\n",i,L,R,K,CD);
  }

  LR = (uint64_t(L) << 32) | R;

  printf("LR: %016lX\n",LR);
  LR = inv_initial_permutation_box(LR);
  printf("plain: %016lX\n",LR);
  return LR;
}