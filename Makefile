cff_flow: cff_flow.cpp
	g++ -O2 -std=c++11 cff_flow.cpp -o cff_flow
clean:
	rm cff_flow
	rm examples/five_users_input_sample.json

