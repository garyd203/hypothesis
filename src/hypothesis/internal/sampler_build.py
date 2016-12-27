import cffi
import os

ffibuilder = cffi.FFI()

SRC = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

assert os.path.basename(SRC) == "src", SRC

with open(
    os.path.join(os.path.dirname(__file__), "sampler.c"),
) as i:
    ffibuilder.set_source(
        "hypothesis.internal._sampler", i.read()

    )

ffibuilder.cdef("""
    void *random_sampler_new(size_t n_items, double *weights);
    void random_sampler_free(void *data);
    size_t random_sampler_sample(void *data, void* mt);
    void random_sampler_debug(void *data);

    void *mersenne_twister_new(uint64_t seed);
    void mersenne_twister_free(void *mt);
""")

if __name__ == "__main__":
    os.chdir(SRC)
    os.environ['CFLAGS'] = '--std=c99'
    ffibuilder.compile(verbose=True)