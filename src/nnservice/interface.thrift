
service Infer {
    list <double> infer(1:list <double> input)
//    bool update_nnmachine(1:i64 nn_id)
    string version()
    oneway void halt()
    bool ping()
}

service NNBackend {
    bool store_nnmachine(1:string name, 2:i32 num_in, 3:i32 num_out, 4:string nnconfig, 5:double score, 6:binary data)
    bool infer_server_ctl(1:string cmd, 2:string name, 3:i64 nn_id)
}
