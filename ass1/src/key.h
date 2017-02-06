#pragma once
#include <cstdint>

uint64_t permutation_choice1_box(uint64_t in){ // bits 8,16,...,64 are used to store parity bit. actual key is 56 bits only
  static const char pc1_table[] = {
    57,49,41,33,25,17,9,
    1,58,50,42,34,26,18,
    10,2,59,51,43,35,27,
    19,11,3,60,52,44,36,
    63,55,47,39,31,23,15,
    7,62,54,46,38,30,22,
    14,6,61,53,45,37,29,
    21,13,5,28,20,12,4
  };
  uint64_t out = 0;
  for(int i=0;i<56;i++){
    out |= ((in >> (64-pc1_table[i])) & 1)<<(55-i);
  }
  return out;
}

uint64_t shift_boxes(int count, uint64_t in){//only lower 56 bits relevant
  // circular-left-shifts first 28 and next 28 bits independently.
  auto low = in & 0xfffffff;
  auto hi = (in >> 28) & 0xfffffff;
  low = ((low << count) | (low >> (28-count))) & 0xfffffff;
  hi = ((hi << count) | (hi >> (28-count))) & 0xfffffff;
  uint64_t out = low | (hi<<28);
  return out;
}

uint64_t inv_shift_boxes(int count, uint64_t in){//only lower 56 bits relevant
  // circular-right-shifts first 28 and next 28 bits independently.
  auto low = in & 0xfffffff;
  auto hi = (in >> 28) & 0xfffffff;
  low = ((low >> count) | (low << (28-count))) & 0xfffffff;
  hi = ((hi >> count) | (hi << (28-count))) & 0xfffffff;
  uint64_t out = low | (hi<<28);
  return out;
}

uint64_t permutation_choice2_box(uint64_t in){ // only lower 56 bits are relevant
  static const char pc2_table[] = {
    14,17,11,24,1,5,
    3,28,15,6,21,10,
    23,19,12,4,26,8,
    16,7,27,20,13,2,
    41,52,31,37,47,55,
    30,40,51,45,33,48,
    44,49,39,56,34,53,
    46,42,50,36,29,32
  };
  uint64_t out = 0;
  for(int i=0;i<48;i++){
    out |= ((in >> (56-pc2_table[i])) & 1)<<(47-i);
  }
  return out;
}

// i can be 1...16.
// CD is themodified CD from previous round. 64-bit input key in case of round 1
uint64_t key_round(int i,uint64_t &CD){
  if(i==1)
  {// CD is actually the 64-bit key with redundant partity bits!
    CD = permutation_choice1_box(CD);
    //printf("CD0: %lX\n", CD);
  }
  const static int shift_table[] = {
    1,1,2,2,
    2,2,2,2,
    1,2,2,2,
    2,2,2,1
  };
  CD = shift_boxes(shift_table[i-1], CD);
  uint64_t K = permutation_choice2_box(CD);
  return K;
}


uint64_t inv_key_round(int i,uint64_t &CD){
  if(i==16)
  {// CD is actually the 64-bit key with redundant partity bits!
    CD = permutation_choice1_box(CD);
    //printf("CD0: %lX\n", CD);
  }
  const static int shift_table[] = {
    1,1,2,2,
    2,2,2,2,
    1,2,2,2,
    2,2,2,1
  };
  uint64_t K = permutation_choice2_box(CD);
  CD = inv_shift_boxes(shift_table[i-1], CD);
  return K;
}