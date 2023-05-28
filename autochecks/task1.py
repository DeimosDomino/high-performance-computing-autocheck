import subprocess, sys

imports_to_add = '''
#include <iostream>
#include <cstdlib> 
#include <vector>
#include <chrono>
#include <thread>
#include <mutex>

'''

code_to_add = '''

int64_t oneThreadSum(int*** matrix, const int n){
    int64_t sum = 0;
    for(int i = 0;i < n; i++){
        for(int j = 0;j < n; j++){
            for(int k = 0;k < n; k++){
                sum += matrix[i][j][k];
            }
        }
    }

    return sum;
}


int main(int argc, char **argv){
    const int count = 100;
    int*** matrix = new int**[count];
    
    int64_t sum = 0;
    
    srand((unsigned)time(NULL));
    for(int i = 0;i < count;i++){
        matrix[i] = new int*[count];
        for(int j = 0;j < count;j++){
            matrix[i][j] = new int[count];
            for(int k = 0;k < count;k++){
                matrix[i][j][k] = rand()% 100;
                sum += matrix[i][j][k];
            }
        }
    }


    auto oneThreadStart = std::chrono::high_resolution_clock::now();
    int64_t oneThread = oneThreadSum(matrix, count);
    auto oneThreadStop = std::chrono::high_resolution_clock::now();
 
    auto oneThreadDuration = std::chrono::duration_cast<std::chrono::microseconds>(oneThreadStop - oneThreadStart);

    std::cout << oneThreadDuration.count() << std::endl;
    
    auto multiThreadStart = std::chrono::high_resolution_clock::now();
    int64_t multiThread = multiThreadSum(matrix, count);
    auto multiThreadStop = std::chrono::high_resolution_clock::now();
    
    auto multiThreadDuration = std::chrono::duration_cast<std::chrono::microseconds>(multiThreadStop - multiThreadStart);

    std::cout << multiThreadDuration.count() << std::endl;

    std::cout << sum << std::endl;
    std::cout << multiThread << std::endl;

    for(int i = 0;i < count;i++){
        for(int j = 0;j < count;j++){
            delete matrix[i][j];
        }
        delete matrix[i];
    }
    delete matrix;

    return 0;
}



'''



def generate():
    return ["OK\n"]

def solve(dataset):
    return 'test'

def check(reply, clue):
    return true

# Write the student code to a file prog.cpp
student_answer = """{{ STUDENT_ANSWER | e('py') }}"""
with open("prog.cpp", "w") as src:
    print(imports_to_add, file=src)
    print(student_answer, file=src)
    print('\n', file=src) 
    print(code_to_add, file=src)

# tests = generate()
# len_tests = len(tests)
correct_count = 0
output = ''
correct_output = ''
return_code = subprocess.check_call("g++ -std=c++14 -pthread prog.cpp -o prog".split())
if return_code != 0:
    print("** Compilation failed. Testing aborted **", file=sys.stderr)
if return_code == 0:
    try:
        output = subprocess.check_output(["./prog"], universal_newlines=True).strip()
        oneThreadDuration, multiThreadDuration, rightSum, multiThreadSum = output.split()
        correct_output = """{{TEST.expected}}""".strip()
    except subprocess.CalledProcessError as e:
        if e.returncode > 0:
            # Ignore non-zero positive return codes
            if e.output:
                print(e.output)
        else:
            # But negative return codes are signals - abort
            if e.output:
                print(e.output, file=sys.stderr)
            if e.returncode < 0:
                print("Task failed with signal", -e.returncode, file=sys.stderr)
            print("** Further testing aborted **", file=sys.stderr)
result = correct_output
if int(multiThreadSum) != int(rightSum):
    result = 'Incorrect sum'
if int(multiThreadDuration) > int(oneThreadDuration)/1.3:
    result = 'Long duration'
if output == correct_output:
    print(correct_output)
else:
    print(result)
