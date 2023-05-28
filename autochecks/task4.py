import subprocess, sys

imports_to_add = '''
#include <iostream>
#include <chrono>
#include <cstdlib> 
#include <thread>
#include <atomic>
#include <vector>


'''

code_to_add = '''

template<class T>
void LockFreeStack<T>::push(const T &value) {
    auto newNode = std::make_shared<Node<T>>(std::move(value));

    std::shared_ptr<Node<T>> first{};
    do {
        first = front;
        newNode->next = first;
    } while (!std::atomic_compare_exchange_weak(&front, &first, newNode));
}

template<class T>
int LockFreeStack<T>::length(){
    std::shared_ptr<Node<T>> cur = this->front;
    int length = 0;
    while(cur != nullptr){
        cur = cur->next;
        length++;
    }
    return length;
}


int main(){
    LockFreeStack<int> stack{};
    srand((unsigned)time(NULL));


    int count = 4; 

    std::vector<std::thread*> threads;

    int rightLength = 0;
    for(int i = 0;i<count;i++){
        int pushCount = rand() % 100;
        rightLength += pushCount;
        
        threads.push_back(new std::thread(
                [&stack, pushCount](){  
                    for(int i = 0;i < pushCount;i++){
                        stack.push(rand() % 100);
                    }
                }   
            )
        );
    };


    for(int i = 0;i < count;i++) threads[i]->join();
    for(int i = 0;i < count;i++) delete threads[i];

    std::string result = "Wrong asnwer";

    if(stack.length() == rightLength) result = "OK";
    std::cout << result << std::endl;
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
if output == correct_output:
    print(correct_output)
else:
    print(output)
