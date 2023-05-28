import subprocess, sys, re

imports_to_add = '''
#include <iostream>
#include <chrono>
#include <cstdlib> 
#include <thread>
#include <atomic>
#include <vector>


'''

code_to_add = '''

template<typename T>
void LockFreeQueue<T>::checkFakeNode(){
    if(this->head == this->tail && this->head != nullptr)
        this->hasFakeNode = true; 
}

template<typename T>
int LockFreeQueue<T>::length(){
    std::shared_ptr<Node<T>> cur = this->head;
    int length = 0;
    while(cur != nullptr){
        cur = cur->next;
        length++;
    }
    return length - this->hasFakeNode;
}

template<typename T>
void LockFreeQueue<T>::push(const T &value) {
    auto node = std::make_shared<Node<T>>(std::move(value));
    while(true){
        std::shared_ptr<Node<T>> last = this->tail;
        std::shared_ptr<Node<T>> next = last->next;
        if(next == nullptr){
            if(std::atomic_compare_exchange_weak(&last->next, &next, node)){
                std::atomic_compare_exchange_weak(&this->tail, &last, node);
                return;
            }
        } else {
            std::atomic_compare_exchange_weak(&tail, &last, next);
        }
    }

}

int main(){
    LockFreeQueue<int> queue{};
    queue.checkFakeNode();
    srand((unsigned)time(NULL));

    for(int i=0;i<400;i++){
        queue.push(i);
    }


    int count = 4; 

    std::vector<std::thread*> threads;

    int rightLength = 400;
    for(int i = 0;i<count;i++){
        int popCount = rand() % 100;
        rightLength -= popCount;
        
        threads.push_back(new std::thread(
                [&queue, popCount](){  
                    for(int i = 0;i < popCount;i++){
                        queue.pop();
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
    int length();
    void checkFakeNode();
    void push(const T &value);
'''

splitted = re.split(r'LockFreeQueue\s*{', student_answer)
student_answer = splitted[0] + 'LockFreeQueue {' + functions_to_add + splitted[1]

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
