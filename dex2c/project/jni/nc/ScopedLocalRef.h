#ifndef SCOPED_LOCAL_REF_H_included
#define SCOPED_LOCAL_REF_H_included

#include "jni.h"

#include <stddef.h>

// A smart pointer that deletes a JNI local reference when it goes out of scope.
template<typename T>
class ScopedLocalRef {
public:
    ScopedLocalRef(JNIEnv* env, T localRef) : mEnv(env), mLocalRef(localRef) {
    }

    ~ScopedLocalRef() {
        reset();
    }

    void reset(T ptr = NULL) {
        if (ptr != mLocalRef) {
            if (mLocalRef != NULL) {
                mEnv->DeleteLocalRef(mLocalRef);
            }
            mLocalRef = ptr;
        }
    }

    T release() __attribute__((warn_unused_result)) {
        T localRef = mLocalRef;
        mLocalRef = NULL;
        return localRef;
    }

    T get() const {
        return mLocalRef;
    }

private:
    JNIEnv* mEnv;
    T mLocalRef;

    // Disallow copy and assignment.
    ScopedLocalRef(const ScopedLocalRef&);
    void operator=(const ScopedLocalRef&);
};

#endif  // SCOPED_LOCAL_REF_H_included
