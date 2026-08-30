program run_MvsT

    ! Perform the MvsT simulation.
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
    use physics,     only: T_, H_, SH_
    use integration, only: evolution
    integer             :: N, X1, X2
    real*8              :: Ti, Tf, HS, H0, HK, alp, dt, params(10)
    real*8, allocatable :: Rm(:), Rp(:), Om(:), Op(:), Mu(:)
    real*8, allocatable :: Em_ZFC(:, :), Em_FC(:, :), En_ZFC(:, :), En_FC(:, :), SH(:)
    real*8, allocatable :: signal_t(:), signal_H(:, :), signal_T0(:)
    real*8              :: t, tt, T0, HS_ZFC(0:2), HS_FC(0:2), H(0:2)
    integer             :: k, k1, k2
    integer(HID_T)      :: file_id
    character(len=100)  :: file_name

!-----------------------------------------------------------------------------------------------------

    ! Threads
#ifdef THREADS
    call omp_set_num_threads(THREADS)
#endif

!-----------------------------------------------------------------------------------------------------

    ! Read Simulation File
    call h5_open('./solvers/llg/temporal/Simulation.h5', file_id)

    ! Read External Parameters
    call h5_read_1d('/Parameters/External', file_id, 10, params)
    N   = int(params(1))
    Ti  = params(2)
    Tf  = params(3)
    HS  = params(4)
    H0  = params(5)
    HK  = params(6)
    alp = params(7)
    dt  = params(8)
    X1  = int(params(9))
    X2  = int(params(10))

    ! Allocate Arrays
    allocate(Rm(0:N-1), Rp(0:N-1), Om(0:N-1), Op(0:N-1), Mu(0:N-1))
    allocate(Em_ZFC(0:2, 0:N-1), Em_FC(0:2, 0:N-1), En_ZFC(0:2, 0:N-1), En_FC(0:2, 0:N-1), SH(0:N-1))
    allocate(signal_t(0:X1-1), signal_H(0:2, 0:X1-1), signal_T0(0:X1-1))

    ! Read Intrinsic Parameters
    call h5_read_1d('/Parameters/Intrinsic/Rm', file_id, N, Rm)
    call h5_read_1d('/Parameters/Intrinsic/Rp', file_id, N, Rp)
    call h5_read_1d('/Parameters/Intrinsic/Ωm', file_id, N, Om)
    call h5_read_1d('/Parameters/Intrinsic/Ωp', file_id, N, Op)
    call h5_read_1d('/Parameters/Intrinsic/μ', file_id, N, Mu)

    ! Read Initial Conditions
    call h5_read_2d('/Microstates/ZFC/Em/Initial', file_id, 3, N, Em_ZFC)
    call h5_read_2d('/Microstates/ZFC/En/Initial', file_id, 3, N, En_ZFC)
    call h5_read_2d('/Microstates/FC/Em/Initial', file_id, 3, N, Em_FC)
    call h5_read_2d('/Microstates/FC/En/Initial', file_id, 3, N, En_FC)

!-----------------------------------------------------------------------------------------------------

    ! Physical Properties
    tt     = X1 * X2 * dt           
    HS_ZFC = H_(0.0d0, 0.0d0, 0.0d0)
    HS_FC  = H_(HS, 0.0d0, 0.0d0)    
    H      = H_(H0, 0.0d0, 0.0d0) 

!-----------------------------------------------------------------------------------------------------

    ! Cooling
    t  = 0.0d0
    T0 = T_(Ti, Tf, tt, t)

    !$omp parallel private(k1, k2)
    ! Physical Properties
    call SH_(N, Mu, T0, alp, dt, SH)

    do k2 = 1, 10*X2
    
        call evolution(N, Em_ZFC, En_ZFC, SH, HS_ZFC, HS_ZFC, HK, alp, dt)
        call evolution(N, Em_FC, En_FC, SH, HS_FC, HS_FC, HK, alp, dt)
        
    end do

    !$omp single
    ! Save ZFC/FC Cooling Microstates
    call h5_write_2d('/Microstates/ZFC/Em/Cooling', file_id, 3, N, Em_ZFC)
    call h5_write_2d('/Microstates/ZFC/En/Cooling', file_id, 3, N, En_ZFC)
    call h5_write_2d('/Microstates/FC/Em/Cooling', file_id, 3, N, Em_FC)
    call h5_write_2d('/Microstates/FC/En/Cooling', file_id, 3, N, En_FC)

    ! Evolution
    k = 0
    !$omp end single

    do k1 = 1, X1
        do k2 = 1, X2

            !$omp single
            T0 = T_(Ti, Tf, tt, t)
            t  = t + dt
            !$omp end single

            call SH_(N, Mu, T0, alp, dt, SH)

            call evolution(N, Em_ZFC, En_ZFC, SH, H, H, HK, alp, dt)
            call evolution(N, Em_FC, En_FC, SH, H, H, HK, alp, dt)
            
        end do

        !$omp single
        ! Signals
        signal_t(k)    = t
        signal_H(:, k) = H
        signal_T0(k)   = T0

        ! Save ZFC/FC Evolution Microstates
        write(file_name, '(I3.3)') k1
        call h5_write_2d('/Microstates/ZFC/Em/' // file_name, file_id, 3, N, Em_ZFC)
        call h5_write_2d('/Microstates/ZFC/En/' // file_name, file_id, 3, N, En_ZFC)
        call h5_write_2d('/Microstates/FC/Em/' // file_name, file_id, 3, N, Em_FC)
        call h5_write_2d('/Microstates/FC/En/' // file_name, file_id, 3, N, En_FC)

        k = k + 1
        !$omp end single

    end do
    !$omp end parallel

!-----------------------------------------------------------------------------------------------------

    ! Save Signals
    call h5_write_1d('/Signals/Time', file_id, X1, signal_t)
    call h5_write_2d('/Signals/Magnetic_Field', file_id, 3, X1, signal_H)
    call h5_write_1d('/Signals/Temperature', file_id, X1, signal_T0)

!-----------------------------------------------------------------------------------------------------

    ! Deallocate Arrays and Close Files
    deallocate(Rm, Rp, Om, Op, Mu, Em_ZFC, Em_FC, En_ZFC, En_FC, SH)
    deallocate(signal_t, signal_H, signal_T0)
    call h5_close(file_id)

!-----------------------------------------------------------------------------------------------------

end program run_MvsT