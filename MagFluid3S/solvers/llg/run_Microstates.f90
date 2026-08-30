program run_Microstates

    ! Perform the Microstates simulation.
    !
    ! Input:
    ! - Simulation.h5
    !
    ! Output:
    ! - Simulation.h5
    !
    ! Used by:
    ! - libs.base.run.run
    !
    ! Last Updated: 
    ! - 16/08/2026

    use hdf5_io
    use physics,     only: H_, SH_
    use integration, only: evolution
    integer             :: N, X2
    real*8              :: T0, H0, HK, alp, dt, params(7)
    real*8, allocatable :: Rm(:), Rp(:), Om(:), Op(:), Mu(:)
    real*8, allocatable :: Em(:, :), En(:, :), SH(:)
    real*8, allocatable :: signal_t(:), signal_H(:, :), signal_T0(:)
    real*8              :: t, H(0:2)
    integer             :: k, k2
    integer(HID_T)      :: file_id
    character(len=100)  :: file_name

!----------------------------------------------------------------------------

    ! Threads
#ifdef THREADS
    call omp_set_num_threads(THREADS)
#endif

!----------------------------------------------------------------------------

    ! Read Simulation File
    call h5_open('./solvers/llg/temporal/Simulation.h5', file_id)

    ! Read External Parameters
    call h5_read_1d('/Parameters/External', file_id, 7, params)
    N   = int(params(1))
    T0  = params(2)
    H0  = params(3)
    HK  = params(4)
    alp = params(5)
    dt  = params(6)
    X2  = int(params(7))

    ! Allocate Arrays
    allocate(Rm(0:N-1), Rp(0:N-1), Om(0:N-1), Op(0:N-1), Mu(0:N-1))
    allocate(Em(0:2, 0:N-1), En(0:2, 0:N-1), SH(0:N-1))
    allocate(signal_t(0:X2-1), signal_H(0:2, 0:X2-1), signal_T0(0:X2-1))

    ! Read Intrinsic Parameters
    call h5_read_1d('/Parameters/Intrinsic/Rm', file_id, N, Rm)
    call h5_read_1d('/Parameters/Intrinsic/Rp', file_id, N, Rp)
    call h5_read_1d('/Parameters/Intrinsic/Ωm', file_id, N, Om)
    call h5_read_1d('/Parameters/Intrinsic/Ωp', file_id, N, Op)
    call h5_read_1d('/Parameters/Intrinsic/μ', file_id, N, Mu)

    ! Read Initial Conditions
    call h5_read_2d('/Microstates/Em/Initial', file_id, 3, N, Em)
    call h5_read_2d('/Microstates/En/Initial', file_id, 3, N, En)

!----------------------------------------------------------------------------

    ! Physical Properties
    H = H_(H0, 0.0d0, 0.0d0)
    
!----------------------------------------------------------------------------

    !$omp parallel private(k2)
    ! Physical Properties
    call SH_(N, Mu, T0, alp, dt, SH)

    !$omp single
    ! Evolution
    k = 0
    t = 0.0d0
    !$omp end single

    do k2 = 1, X2

        !$omp single
        t = t + dt
        !$omp end single

        call evolution(N, Em, En, SH, H, H, HK, alp, dt)

        !$omp single
        ! Signals
        signal_t(k)    = t
        signal_H(:, k) = H
        signal_T0(k)   = T0

        ! Save Evolution Microstates
        write(file_name, '(I4.4)') k2
        call h5_write_2d('/Microstates/Em/' // file_name, file_id, 3, N, Em)
        call h5_write_2d('/Microstates/En/' // file_name, file_id, 3, N, En)

        k = k + 1
        !$omp end single

    end do
    !$omp end parallel

!----------------------------------------------------------------------------

    ! Save Signals
    call h5_write_1d('/Signals/Time', file_id, X2, signal_t)
    call h5_write_2d('/Signals/Magnetic_Field', file_id, 3, X2, signal_H)
    call h5_write_1d('/Signals/Temperature', file_id, X2, signal_T0)

!----------------------------------------------------------------------------

    ! Deallocate Arrays and Close Files
    deallocate(Rm, Rp, Om, Op, Mu, Em, En, SH)
    deallocate(signal_t, signal_H, signal_T0)
    call h5_close(file_id)

!----------------------------------------------------------------------------

end program run_Microstates