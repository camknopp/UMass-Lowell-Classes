#ifndef TOMBSTONES_H
#define TOMBSTONES_H

#include <iostream>

// Defintion of Tomb for Pointer class
template <class T>
struct Tomb
{
    T *content;
    int ref_cnt;
    bool used;

    Tomb<T>()
    {
        content = NULL;
        ref_cnt = 0;
    }
    ~Tomb()
    {
        content = NULL;
        ref_cnt = 0;
    }
};

template <class T>
class Pointer
{
public:
    Tomb<T> *ptr;
    Pointer<T>()
    {
        ptr = new Tomb<T>();
        ptr->used = false;
    }                         // default constructor
    Pointer<T>(Pointer<T> &p) // copy constructor
    {
        if (p.ptr->used)
        {
            ptr = p.ptr;
            if (ptr->ref_cnt != 0)
            {
                ptr->ref_cnt++;
            }
        }
        else
        {
            std::cout << "Dangling reference exception" << std::endl;
            exit(1);
        }
    }
    Pointer<T>(T *t) // bootstrapping constructor
    {
        ptr = new Tomb<T>();
        ptr->used = true;
        ptr->content = t;
        if (ptr->content == NULL)
        {
            ptr->ref_cnt = 0;
        }
        else
        {
            ptr->ref_cnt = 1;
        }
    }
    // argument should always be a call to new
    ~Pointer<T>() // destructor
    {
        ptr->ref_cnt--;
        if (ptr->used && ptr->ref_cnt == 0)
        {
            std::cout << "Memory leak exception" << std::endl;
            exit(1);
        }
        else
        {
            ptr = NULL;
        }
    }
    T &operator*() const // dereferencing
    {
        if (!ptr->used)
        {
            std::cout << "Dangling reference exception" << std::endl;
            exit(1);
        }
        else if (ptr->ref_cnt == 0)
        {
            std::cout << "Memory leak exception" << std::endl;
            exit(1);
        }
        else
        {
            return *(ptr->content);
        }
    }
    T *operator->() const // field dereferencing
    {
        if (!ptr->used)
        {
            std::cout << "Dangling reference exception" << std::endl;
            exit(1);
        }
        else if (ptr->ref_cnt == 0)
        {
            std::cout << "Memory leak exception" << std::endl;
            exit(1);
        }
        else
        {
            return ptr->content;
        }
    }
    Pointer<T> &operator=(const Pointer<T> &p) // assignment
    {
        ptr->ref_cnt--;
        if (ptr->ref_cnt == 0)
        {
            std::cout << "Memory leak exception" << std::endl;
            exit(1);
        }
        ptr = p.ptr;
        ptr->ref_cnt++;
        

        if (!ptr->used)
        {
            std::cout << "Dangling reference exception" << std::endl;
            exit(1);
        }
        return *this;
    }
    friend void free(Pointer<T> &p) // delete pointed-at object
    {
        if (p.ptr->used)
        {
            delete p.ptr->content;
            p.ptr->used = false;
        }
        else
        {
            std::cout << "Dangling reference exception" << std::endl;
            exit(1);
        }
    }
    // This is essentially the inverse of the new inside the call to
    // the bootstrapping constructor. It should delete the pointed-to
    // object (which should in turn call its destructor).
    // equality comparisons:
    bool operator==(const Pointer<T> &p) const
    {
        if (!ptr->used || !p.ptr->used)
        {
            std::cout << "Dangling reference exception" << std::endl;
            exit(1);
        }
        else
        {
            return p.ptr->content == ptr->content;
        }
    }
    bool operator!=(const Pointer<T> &p) const
    {
        if (!ptr->used || !p.ptr->used)
        {
            std::cout << "Dangling reference exception" << std::endl;
            exit(1);
        }
        else
        {
            return p.ptr->content != ptr->content;
        }
    }
    bool operator==(const int x) const
    {
        if (ptr->content == NULL && x == 0)
            return true;
        return false;
    }
    // true iff Pointer is null and int is zero
    bool operator!=(const int x) const
    {
        if (ptr->content == NULL && x == 0)
            return false;
        return true;
    }
    // false iff Pointer is null and int is zero
};

template <class T>
bool operator==(const int n, const Pointer<T> &t) { return t == n; }

template <class T>
bool operator!=(const int n, const Pointer<T> &t) { return t != n; }

#endif