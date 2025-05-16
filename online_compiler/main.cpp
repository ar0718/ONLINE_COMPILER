#include <iostream>
using namespace std;

int main() {
    int nums[5];
    for(int i = 0; i < 5; i++) {
        cin >> nums[i];
    }

    int max_num = nums[0];
    for(int i = 1; i < 5; i++) {
        if(nums[i] > max_num) {
            max_num = nums[i];
        }
    }

    cout << max_num << endl;
    return 0;
}