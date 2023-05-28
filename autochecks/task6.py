import subprocess, sys, re

imports_to_add = '''
#include <iostream>
#include <chrono>
#include <cstdlib> 
#include <thread>
#include <atomic>
#include <vector>
#include <mutex>


'''

code_to_add = '''

template<typename T>
void ThreadsafeQueue<T>::checkFakeNode(){
    if(this->head == this->tail && this->head != nullptr)
        this->hasFakeNode = true; 
}

template<typename T>
int ThreadsafeQueue<T>::length(){
    std::shared_ptr<Node<T>> cur = this->head;
    int length = 0;
    while(cur != nullptr){
        cur = cur->next;
        length++;
    }
    return length - this->hasFakeNode;
}


int main(){
    ThreadsafeQueue<int> queue{};
    queue.checkFakeNode();
    srand((unsigned)time(NULL));


    int count = 4; 

    std::vector<std::thread*> threads;

    int rightLength = 0;
    for(int i = 0;i<count;i++){
        int pushCount = rand() % 100;
        rightLength += pushCount;
        
        threads.push_back(new std::thread(
                [&queue, pushCount](){  
                    for(int i = 0;i < pushCount;i++){
                        queue.push(rand() % 100);
                    }
                }   
            )
        );
    };

    for(int i = 0;i < count;i++) threads[i]->join();
    for(int i = 0;i < count;i++) delete threads[i];

    std::string result = "Wrong asnwer";


    if(queue.length() == rightLength) result = "OK";
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

functions_to_add = '''
public:
    bool hasFakeNode = false;
    void checkFakeNode();
    int length();
'''

splitted = re.split(r'ThreadsafeQueue\s*{', student_answer)
student_answer = splitted[0] + 'ThreadsafeQueue {' + functions_to_add + splitted[1]

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
