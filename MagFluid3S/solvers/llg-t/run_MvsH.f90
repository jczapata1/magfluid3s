program run_MvsH

    ! Perform the MvsH simulation.
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
    use physics,     only: H_, ETA_, Z_, SH_, S0_
    use integration, only: evolution
    integer             :: N, X0, X1, X2
    real*8              :: T0, H0, HK, alp, dt, f, params(10)
    real*8, allocatable :: Rm(:), Rp(:), Om(:), Op(:), Mu(:)
    real*8, allocatable :: Em(:, :), En(:, :), Z(:), SH(:), S0(:)
    real*8, allocatable :: signal_t(:), signal_H(:, :), signal_T0(:)
    real*8              :: t, eta, Ha(0:2), Hb(0:2)
    integer             :: k, k0, k1, k2
    integer(HID_T)      :: file_id
    character(len=100)  :: file_name

!--------------------------------------------------------------------------------

    ! Threads
#ifdef THREADS
    call omp_set_num_threads(THREADS)
#endif

!--------------------------------------------------------------------------------

    ! Read Simulation File
    call h5_open('./solvers/llg-t/temporal/Simulation.h5', file_id)

    ! Read External Parameters
    call h5_read_1d('/Parameters/External', file_id, 10, params)
    N   = int(params(1))
    T0  = params(2)
    H0  = params(3)
    HK  = params(4)
    alp = params(5)
    dt  = params(6)
    X0  = int(params(7))
    X1  = int(params(8))
    X2  = int(params(9))
    f   = params(10)

    ! Allocate Arrays
    allocate(Rm(0:N-1), Rp(0:N-1), Om(0:N-1), Op(0:N-1), Mu(0:N-1))
    allocate(Em(0:2, 0:N-1), En(0:2, 0:N-1), Z(0:N-1), SH(0:N-1), S0(0:N-1))
    allocate(signal_t(0:X0*X1-1), signal_H(0:2, 0:X0*X1-1), signal_T0(0:X0*X1-1))

    ! Read Intrinsic Parameters
    call h5_read_1d('/Parameters/Intrinsic/Rm', file_id, N, Rm)
    call h5_read_1d('/Parameters/Intrinsic/Rp', file_id, N, Rp)
    call h5_read_1d('/Parameters/Intrinsic/Ωm', file_id, N, Om)
    call h5_read_1d('/Parameters/Intrinsic/Ωp', file_id, N, Op)
    call h5_read_1d('/Parameters/Intrinsic/μ', file_id, N, Mu)

    ! Read Initial Conditions
    call h5_read_2d('/Microstates/Em/Initial', file_id, 3, N, Em)
    call h5_read_2d('/Microstates/En/Initial', file_id, 3, N, En)

!--------------------------------------------------------------------------------

    ! Physical Properties
    eta = ETA_(T0)
    
!--------------------------------------------------------------------------------

    !$omp parallel private(k0, k1, k2)
    ! Physical Properties
    call Z_(N, Op, eta, Z)          
    call SH_(N, Mu, T0, alp, dt, SH)
    call S0_(N, Z, T0, dt, S0)      

    !$omp single
    ! Saturation
    t  = 0.0d0
    Ha = H_(H0, f, t)
    !$omp end single

    do k2 = 1, 10*X2
        call evolution(N, Mu, Em, En, Z, SH, S0, Ha, Ha, HK, alp, dt)
    end do

    !$omp single
    ! Save Saturation Microstates
    call h5_write_2d('/Microstates/Em/Saturation', file_id, 3, N, Em)
    call h5_write_2d('/Microstates/En/Saturation', file_id, 3, N, En)

    ! Evolution
    k = 0
    !$omp end single

    do k0 = 1, X0
        do k1 = 1, X1
            do k2 = 1, X2

                !$omp single
                Ha = H_(H0, f, t)
                Hb = H_(H0, f, t + dt)
                t  = t + dt
                !$omp end single

                call evolution(N, Mu, Em, En, Z, SH, S0, Ha, Hb, HK, alp, dt)
                
            end do

            !$omp single
            ! Signals
            signal_t(k)    = t
            signal_H(:, k) = Hb
            signal_T0(k)   = T0

            ! Save Evolution Microstates
            write(file_name, '(I2.2,A,I3.3)') k0, '_', k1
            call h5_write_2d('/Microstates/Em/' // file_name, file_id, 3, N, Em)
            call h5_write_2d('/Microstates/En/' // file_name, file_id, 3, N, En)

            k = k + 1
            !$omp end single

        end do
    end do
    !$omp end parallel

!--------------------------------------------------------------------------------

    ! Save Signals
    call h5_write_1d('/Signals/Time', file_id, X0*X1, signal_t)
    call h5_write_2d('/Signals/Magnetic_Field', file_id, 3, X0*X1, signal_H)
    call h5_write_1d('/Signals/Temperature', file_id, X0*X1, signal_T0)

!--------------------------------------------------------------------------------

    ! Deallocate Arrays and Close Files
    deallocate(Rm, Rp, Om, Op, Mu, Em, En, Z, SH, S0)
    deallocate(signal_t, signal_H, signal_T0)
    call h5_close(file_id)

!--------------------------------------------------------------------------------

end program run_MvsH